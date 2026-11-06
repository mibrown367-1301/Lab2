# This creates the page for displaying data visualizations.

import plotly.express as px
import streamlit as st
import pandas as pd
import json
import os

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")
st.write("Interact with some of my favorite outdoor adventures and snacks to find the ones best suited to you!")

st.divider()

# PART 1: GRAPHS FROM data.json

# create tabs for part 1 and 2??
tab1, tab2 = st.tabs(["🏔️ Adventure Visuals", "🎒 Trail Snack Survey Results"])

# this is the tab with the part 1 stuff
# static graph here
# note to self: remember to to the advanced visualization (plotly!)
with tab1:
    infile = open("data.json")
    myData = json.load(infile)

    adventures_list = myData["adventures"]
    df = pd.DataFrame(adventures_list)

    st.subheader("Exhaustion Level vs. Satisfaction Level")
    st.caption("Static Visualization with Advanced Element")

    names = [adventure["name"] for adventure in adventures_list]
    exhaustion = [adventure["exhaustionLevel"] for adventure in adventures_list]
    satisfaction = [adventure["satisfactionLevel"] for adventure in adventures_list]
    locations = [adventure["location"] for adventure in adventures_list]
    tripTypes = [adventure["tripType"] for adventure in adventures_list]

    fig = px.scatter(
        x = exhaustion,
        y = satisfaction,
        labels = {"x": "Exhaustion Level", "y": "Satisfaction Level"},
        title = "Adventure Overview",
        hover_name = names,
        hover_data = {"Location": locations, "Type": tripTypes,},
    )

    st.plotly_chart(fig)

    st.divider()

# dynamic graph of part 1 here

    st.subheader("Adventure Matcher")
    st.write("Find your next outdoor adventure based on what you're looking for!")
    st.caption("(Interact with the Adventure Matcher to see a dynamic visualization appear! Then keep scrolling to learn more.)")

    st.write(" ")

    tripTypesList = ["All"]
    for adventure in adventures_list:
        if adventure["tripType"] not in tripTypesList:
            tripTypesList.append(adventure["tripType"])

    chosenType = st.selectbox("What kind of adventure are you looking for?", tripTypesList)

    targetExhaustion = st.slider("How tired are you willing to be? (Exhaustion Level)", 0.0, 10.0, 10.0)

    if "results" not in st.session_state:
        st.session_state.results = []
    if "searched" not in st.session_state:
        st.session_state.searched = False
    if "notebook" not in st.session_state:
        st.session_state.notebook = []

    clicked = st.button("Find My Adventure")

    if clicked:
        st.session_state.results = []

        for adventure in adventures_list:
            if (chosenType == "All" or adventure["tripType"] == chosenType) and (abs(adventure["exhaustionLevel"]-targetExhaustion) <= 1.5):
                st.session_state.results.append(adventure)

        st.session_state.searched = True
        
    if st.session_state.searched:
        st.write(f"We found {len(st.session_state.results)} adventures for you. Save them to your notebook to learn more.")

        if st.session_state.results:
            for adventure in st.session_state.results:
                with st.container(border=True):
                    st.write(f"**{adventure['name']}** ({adventure['tripType']})")
                    st.write(f"Location: {adventure['location']} | Exhaustion: "
                             f"{adventure['exhaustionLevel']} | Satisfaction: "
                             f" {adventure['satisfactionLevel']}")

                    if st.button(f"Save {adventure['name']} to Notebook", key=f"save_{adventure['name']}",):
                        if adventure not in st.session_state.notebook:
                            st.session_state.notebook.append(adventure)
                            st.success(f"Saved {adventure['name']} to your notebook!")
                        else:
                            st.info("That trip is already in your notebook!")
        else:
            st.info("No adventures match that exhaustion range right now. Try adjusting the slider!")

    st.divider()

    st.header("Your Saved Trip Notebook")

    if st.session_state.notebook:
        st.write(f"You have {len(st.session_state.notebook)} saved adventure(s).")

        st.subheader("Saved Adventures Map")
        st.caption("Dynamic Visualization (keep scrolling to view the rest of your notebook!)")
        notebook_df = pd.DataFrame(st.session_state.notebook)

# EXTRA CREDIT!!!!!
    # to do: use the st.metric to do summary of stats from dynamic graph
    # can compare user's average exhaustion and satisfaction levels to the average of all possible trips?

        overallMeanExhaustion = df["exhaustionLevel"].mean()
        overallMeanSatisfaction = df["satisfactionLevel"].mean()
        
        meanExhaustion = round(notebook_df["exhaustionLevel"].mean(), 1)
        meanSatisfaction = round(notebook_df["satisfactionLevel"].mean(), 1)

        ex_delta = round(meanExhaustion - overallMeanExhaustion, 1)
        sat_delta = round(meanSatisfaction - overallMeanSatisfaction, 1)
        
        statColumn1, statColumn2 = st.columns(2)
        with statColumn1:
            st.metric(label = "Mean Exhaustion Level", value = meanExhaustion, delta = f"{ex_delta} compared to overall average")
        with statColumn2:
            st.metric(label = "Mean Satisfaction Level", value = meanSatisfaction, delta = f"{sat_delta} compared to overall average")

        st.divider()
        st.map(notebook_df)
        st.divider()

        for saved_trip in st.session_state.notebook:
            with st.container(border=True):
                col1, col2 = st.columns([2,1])
                with col1:
                    st.write(f"**{saved_trip['name']}** - {saved_trip['tripType']}")
                    st.write(f"Location: {saved_trip['location']}")
                    st.write(f"Distance: {saved_trip['distanceMiles']} miles | Elevation Gained: {saved_trip['elevationGainFeet']} feet")
                    st.write(f"Exhaustion: {saved_trip['exhaustionLevel']} | Satisfaction: {saved_trip['satisfactionLevel']}")          
                with col2:
                    st.image(saved_trip["image"])
    else:
        st.info("Your notebook is empty. Search for trips and click 'Save to Notebook' to build your itinerary!")


# TO DO LIST:
        # advanced visualization (REQUIRED) - DONE
        # figure out session states!! (REQUIRED) - DONE
        # maybe add images - DONE
        # add more options? - DONE
        # change range for adventure picker??
        # EXTRA CREDIT BY USING ST.METRIC!! - DONE

        # ask TA: does the notebook thing count as visualization?
            # otherwise could do a map and plot the locations of the adventures?
        # also ask if it's okay that the dynamic visualization only pops up after user input - DONE


# PART 2: GRAPHS FROM data.csv

# snack survey results start here:

with tab2:
    st.subheader("Trail Snack Survey Results")
    st.write("Here is what people are bringing on our adventure based on survey results!")

    if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
        snackTable = pd.read_csv('data.csv')

        #static planning here!!!
        
        if len(snackTable) > 0:
            st.markdown("### Overall Snack Popularity (static)")
            snackCounts = {}
            for snack in snackTable["Value"]:
                if snack in snackCounts:
                    snackCounts[snack] += 1
                else:
                    snackCounts[snack] = 1

            snackNames = list(snackCounts.keys())
            snackTotals = list(snackCounts.values())

            staticPieFigure = px.pie(
                names=snackNames,
                values=snackTotals,
                title="Proportion of All Submitted Trail Snacks (with advanced visualization)"
            )
            st.plotly_chart(staticPieFigure)
            st.divider()




            #dynamic graph brainstorming...

            st.markdown("### Dynamic Snack Explorer")
            st.caption ("See the popularity of certain snacks in the categories you prefer")

            if "flavorChoice" not in st.session_state:
                st.session_state.flavorChoice = "All"
            if "eneryChoice" not in st.session_state:
                st.session_state.energyChoice = "All"

            flavorOptions = ["All", "Salty", "Sweet", "Savory", "Other"]
            energyOptions = ["All", "Quick Energy", "Sustained Energy", "Other"]
            userFlavor = st.selectbox("Select Flavor Category:", flavorOptions, key="flavorSelectBox")
            userEnergy = st.selectbox("Select Energy Type:", energyOptions, key="energySelectBox")
            st.session_state.flavorChoice = userFlavor
            st.session_state.energyChoice = userEnergy

            filteredList = []
            for index, surveyRow in snackTable.iterrows():
                snackName = str(surveyRow["Value"]).lower()
                
                if "chip" in snackName or "pretzel" in snackName or "peanut" in snackName or "salt" in snackName:
                    snackFlavor = "Salty"
                elif "tootsie" in snackName or "fruit" in snackName or "fig" in snackName or "cookie" in snackName or "candy" in snackName or "chocolate" in snackName:
                    snackFlavor = "Sweet"
                elif "jerky" in snackName or "tuna" in snackName or "meat" in snackName or "cheese" in snackName:
                    snackFlavor = "Savory"
                else:
                    snackFlavor = "Other"

                if "tootsie" in snackName or "fruit" in snackName or "chip" in snackName:
                    snackEnergy = "Quick Energy"
                elif "trail mix" in snackName or "granola" in snackName or "protein" in snackName or "jerky" in snackName or "nut" in snackName or "peanut" in snackName or "tuna" in snackName or "fig" in snackName:
                    snackEnergy = "Sustained Energy"
                else:
                    snackEnergy = "Other"

                matchesFlavor = (st.session_state.flavorChoice == "All" or snackFlavor == st.session_state.flavorChoice)
                matchesEnergy = (st.session_state.energyChoice == "All" or snackEnergy == st.session_state.energyChoice)
                if matchesFlavor and matchesEnergy:
                    filteredList.append(surveyRow)

            st.write(f"Showing results for Flavor: **{st.session_state.flavorChoice}** | Energy: **{st.session_state.energyChoice}**")
            if len(filteredList) > 0:
                filteredTable = pd.DataFrame(filteredList)
                
                filteredCounts = {}
                for snackItem in filteredTable["Value"]:
                    if snackItem:
                        if snackItem in filteredCounts:
                            filteredCounts[snackItem] += 1
                        else:
                            filteredCounts[snackItem] = 1

                voteValues = list(filteredCounts.values())
                if voteValues:
                    meanVotes = round(pd.Series(voteValues).mean(), 1)
                    medianVotes = round(pd.Series(voteValues).median(), 1)
                else:
                    meanVotes = 0
                    medianVotes = 0

                metricCol1, metricCol2 = st.columns(2)
                with metricCol1:
                    st.metric(label="Mean Votes per Snack", value=meanVotes)
                with metricCol2:
                    st.metric(label="Median Votes per Snack", value=medianVotes)

                barNames = list(filteredCounts.keys())
                barTotals = list(filteredCounts.values())

                dynamicBarFigure = px.bar(x=barNames,y=barTotals,
                    labels={"x": "Snack Type", "y": "Number of Votes"},
                    title=f"Snacks for Flavor: {st.session_state.flavorChoice} | Energy: {st.session_state.energyChoice}"
                )
                
                st.plotly_chart(dynamicBarFigure)

            else:
                st.info("No snacks match this specific combination of categories. Try adjusting your filters!")

        else:
            st.info("No survey submissions yet! Head over to the Survey page to add some data.")
    else:
        st.info("The 'data.csv' file is currently empty or does not exist.")
