import random
import logging
from typing import Any, Text, Dict, List
import inspect
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin
# from a import GetAns

# Set up logging
logger = logging.getLogger(__name__)
# getAns = GetAns()

# Firebase Initialization
if not firebase_admin._apps:
    cred = credentials.Certificate("/Users/sharatrk/Desktop/CricBot/frontend/src/firebase/serviceAccountKey.json")
    initialize_app(cred)

db = firestore.client()

# Team name mapping
team_name_mapping = {
    "csk": "Chennai Super Kings",
    "mi": "Mumbai Indians",
    "rcb": "Royal Challengers Bengaluru",
    "kkr": "Kolkata Knight Riders",
    "dc": "Delhi Capitals",
    "srh": "Sunrisers Hyderabad",
    "rr": "Rajasthan Royals",
    "pk": "Punjab Kings",
    "pbks": "Punjab Kings",
    "gt": "Gujarat Titans",
    "lsg": "Lucknow Super Giants",
    "dch": "Deccan Chargers",
    "ktk": "Kochi Tuskers Kerala",
    "pwi": "Pune Warriors India",
    "rps": "Rising Pune Supergiants",
    "gl": "Gujarat Lions"
}

# Ground name mapping for common abbreviations
ground_name_mapping = {
    "chepauk": "MA Chidambaram Stadium",
    "wankhede": "Wankhede Stadium",
    "chinnaswamy": "M Chinnaswamy Stadium",
    "eden gardens": "Eden Gardens",
    "kotla": "Arun Jaitley Stadium",
    "feroz shah kotla": "Arun Jaitley Stadium",
    "hyderabad": "Rajiv Gandhi International Stadium",
    "jaipur": "Sawai Mansingh Stadium",
    "mohali": "Punjab Cricket Association IS Bindra Stadium"
}

# Collection group mapping
collection_groups = {
    # Group 1: Batsman Related
    "batsman_records": [
        "20_to_50_Consecutive_Innings", "50_On_Debut", "Batsman_Dismiss_1st_Ball_Innings",
        "First_50_Innings_Count", "highest_strike_rate_innings", "Innings_Take_to_1st_100",
        "Openers_50_And_Duck", "Opening_Pairs_50_Plus_Partnerships", "Scoring_99_an_Innings",
        "Top_Scorers_By_Position", "Yearwise_Highest_Averages"
    ],
    # Group 2: Batsman Related
    "batsman_milestones": [
        "1000_to_8000_Runs", "Best_Strike_Rate", "Career_Partnerships",
        "Fastest_Centuries", "Fastest_Fifties", "Fastest_Milestones_Runs",
        "Highest_Scores_Innings", "Highest_Strike_Rates_All_Time", "Most_Centuries",
        "Most_Fifties", "Most_Runs_2008_2024", "Most_Runs_From_Boundaries_Per_Innings",
        "Most_Runs_Overall", "Most_Sixes_2008_2024", "Most_Sixes_All_Times"
    ],
    # Group 3: Wicketkeeper Related
    "wicketkeeper_records": [
        "Player_Impact_2008_2010", "Player_Impact_2011_2013", "Player_Impact_2014_2016",
        "Player_Impact_2017_2019", "Player_Impact_2020_2022", "Player_Impact_2023_2024",
        "Wicketkeeper_Highest_Scores", "Wicketkeeper_Most_Dismissals_Per_Innings",
        "Wicketkeeper_Overall_Records_with_Stumpings"
    ],
    # Group 4: Bowler Impact
    "bowler_impact": [
        "2008-2012_Bowler_Impact", "2013-2016_Bowler_Impact", "2017-2021_Bowler_Impact",
        "2022-2024_Bowler_Impact", "Most_4_Wickets_Innings", "Most_Economical",
        "Most_Wickets_1st_50_Matches", "Most_Wickets_Consecutive_Matches",
        "Most_Wickets_in_IPL", "Most_Wickets_Innings"
    ],
    # Group 5: Bowler Related
    "bowler_records": [
        "Best_Economy_Rates_Innings", "Bowler_Best_Strike_Rate", 
        "Bowler_Dismissal_Records", "Fastest_Player_50_Wickets",
        "First_Ball_Wicket", "IPL_Bowlers_Data_2008_2024",
        "IPL_Hat_Tricks", "Lowest_Averages", "Most_Runs_Conceded"
    ],
    # Group 6: IPL Other Records
    "ipl_other_records": [
        "All_Players_Records", "Auctioneers", "Cap_Holders", 
        "Coaches_Overrall", "Grounds_Records", "IPL_Captains_Records",
        "IPL_Players_Overall_Data_2008_2024", "IPL_Team_Captains_Overall_Records",
        "Most_Catch_in_an_Innings", "Most_Ducks_In_Career",
        "Tied_Matches", "Top_Allrounders", "Umpire_Data"
    ],
    # Group 7: Team Match Results
    "team_match_results": [
        "Overall_Match_Results_CSK", "Overall_Match_Results_DC", "Overall_Match_Results_DCH",
        "Overall_Match_Results_GL", "Overall_Match_Results_GT", "Overall_Match_Results_KKR",
        "Overall_Match_Results_KTK", "Overall_Match_Results_LSG", "Overall_Match_Results_MI",
        "Overall_Match_Results_PK", "Overall_Match_Results_PWI", "Overall_Match_Results_RCB",
        "Overall_Match_Results_RPS", "Overall_Match_Results_RR", "Overall_Match_Results_SRH"
    ],
    # Group 8: Team vs All
    "team_vs_all": [
        "CSK_with_All", "DC_with_All", "DCH_with_All", "GL_with_All", "GT_with_All",
        "KKR_with_All", "KTK_with_All", "LSG_with_All", "MI_with_All", "PBKS_with_All",
        "PWI_with_All", "RCB_With_All", "RPS_with_All", "RR_with_All", "SRH_with_All"
    ],
    # Group 9: Team Performance
    "team_performance": [
        "2008_2024", "All_ipl_match_data_yearwise_scorecard", "All_Years_Teams_Performance",
        "Close_Matches_by_Wickets", "End_moment_finish", "Highest_Match_Total_Scores",
        "Highest_Partnerships", "Highest_Run_Chase", "Highest_Scores_Teamwise_Overall",
        "Highest_Scores", "Highest_Successful_Run_Chases", "IPL_Points_Table_2008_2024",
        "Lowest_Scores_IPL", "Lowest_Scores_Teamwise", "One_sided_finish",
        "Top_10_Partnerships_by_Team"
    ]
}

# Flat list of all collections for easy lookup
all_collections = [coll for group in collection_groups.values() for coll in group]

# Field mappings for collection groups
field_mappings = {
    "batsman_records": {
        "player": ["Player_Name", "Player", "Batsman_Name", "Batsman"],
        "team": ["Team", "Team_Name", "Batsman_Team"],
        "runs": ["Runs", "Runs_Scored", "Runs_Consecutive"],
        "date": ["Match_Date", "Debut_Date", "Date"]
    },
    "batsman_milestones": {
        "player": ["Player_Name", "Player"],
        "team": ["Team", "Team_Name", "Team_Names", "Teams"],
        "runs": ["Runs", "Runs_Scored", "Career_Runs"],
        "date": ["Match_Date", "Date"]
    },
    "wicketkeeper_records": {
        "player": ["Player"],
        "team": ["Team", "Teams_Represented"],
        "runs": ["Runs"],
        "date": ["Date", "Match_Date"]
    },
    "bowler_impact": {
        "player": ["Player", "Bowler"],
        "team": ["Team", "Bowler_Team"],
        "wickets": ["Wickets", "Total_Wickets", "Consecutive_Wickets"],
        "economy": ["Economy_Rate"]
    },
    "bowler_records": {
        "player": ["Player", "Bowler"],
        "team": ["Team", "Team_Name", "Bowler_Team"],
        "wickets": ["Wickets"],
        "economy": ["Economy_Rate"]
    },
    "ipl_other_records": {
        "player": ["Name", "Player", "Captain_Name", "Allrounder"],
        "team": ["Team", "Teams", "Team_Names", "Team(s)"],
        "runs": ["Runs"],
        "wickets": ["Wickets"]
    },
    "team_match_results": {
        "team": ["Team"],
        "opponent": ["Versus"],
        "venue": ["Venue"],
        "result": ["Result"],
        "date": ["Date"]
    },
    "team_vs_all": {
        "opponent": ["Against", "Opponent"],
        "ground": ["Ground"],
        "result": ["Total", "No_Result"]
    },
    "team_performance": {
        "team": ["Team", "Batting_Team", "Winner"],
        "opponent": ["Opponent", "Opponent_Team", "Opposing_Team"],
        "venue": ["Venue", "Stadium_Name", "Ground"],
        "runs": ["Runs_Scored", "Score", "Target_Score", "Target"]
    }
}

# Base Firebase Action class
class FirebaseAction(Action):
    def name(self) -> Text:
        return self.__class__.__name__.lower()

    def collection_name(self, team_name=None) -> Text:
        if team_name:
            # Convert team names to collection names
            team_name = team_name.lower() if team_name else ""
            for short_name, full_name in team_name_mapping.items():
                if full_name.lower() in team_name or short_name.lower() == team_name:
                    return f"{short_name.upper()}_with_All"
            return "CSK_with_All"  # Default to CSK if no match
        else:
            # Default collection should be overridden in child classes
            for group, collections in collection_groups.items():
                if hasattr(self, 'group') and self.group == group and collections:
                    return collections[0]
            return "Most_Runs_Overall"  # Default to a common collection

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        raise NotImplementedError

    def standardize_team_name(self, team_name):
        if not team_name:
            return None
        team_name = team_name.lower()
        for short_name, full_name in team_name_mapping.items():
            if short_name.lower() == team_name or full_name.lower() in team_name:
                return full_name
        return team_name.title()

    def standardize_ground_name(self, ground_name):
        if not ground_name:
            return None
        ground_name = ground_name.lower()
        for abbr, full_name in ground_name_mapping.items():
            if abbr.lower() in ground_name:
                return full_name
        return ground_name.title()

    def get_field_mappings(self, collection_name):
        for group, collections in collection_groups.items():
            if collection_name in collections and group in field_mappings:
                return field_mappings[group]
        return {}

    def filter_query(self, query_ref, tracker: Tracker):
        try:
            collection_name = self.collection_name() if not callable(getattr(self, "collection_name")) or len(inspect.signature(self.collection_name).parameters) == 0 else None
            if not collection_name:
                collection_name = "Most_Runs_Overall"  # Default
                
            field_maps = self.get_field_mappings(collection_name)
            
            # Extract slots
            player_name = tracker.get_slot("player_name")
            team_name = tracker.get_slot("team_name")
            year = tracker.get_slot("year")
            match_code = tracker.get_slot("match_code")
            venue = tracker.get_slot("venue")
            opponent = tracker.get_slot("opponent")
            wicket_position = tracker.get_slot("wicket_position")
            runs = tracker.get_slot("runs")
            season = tracker.get_slot("season")
            margin = tracker.get_slot("margin")
            captain_name = tracker.get_slot("captain_name")
            coach_name = tracker.get_slot("coach_name")
            auctioneer_name = tracker.get_slot("auctioneer_name")
            allrounder_name = tracker.get_slot("allrounder_name")
            umpire_name = tracker.get_slot("umpire_name")
            innings = tracker.get_slot("innings")
            opponent_team = tracker.get_slot("opponent_team")
            
            # Apply player name filter with field mapping
            if player_name:
                player_fields = field_maps.get("player", ["Player", "Player_Name", "Name"]) if field_maps else ["Player", "Player_Name", "Name"]
                for field in player_fields:
                    try:
                        return query_ref.where(field, ">=", player_name).where(field, "<=", player_name + "\uf8ff").limit(5)
                    except:
                        continue
                # Default fallback
                return query_ref.where("Player", ">=", player_name).where("Player", "<=", player_name + "\uf8ff").limit(5)
                
            # Apply team name filter with field mapping
            if team_name:
                team_fields = field_maps.get("team", ["Team", "Team_Name", "Team(s)"]) if field_maps else ["Team", "Team_Name", "Team(s)"]
                for field in team_fields:
                    try:
                        return query_ref.where(field, ">=", team_name).where(field, "<=", team_name + "\uf8ff").limit(5)
                    except:
                        continue
                # Default fallback
                return query_ref.where("Team", ">=", team_name).where("Team", "<=", team_name + "\uf8ff").limit(5)
                
            # Other filters
            if year:
                try:
                    return query_ref.where("Year", "==", year).limit(5)
                except:
                    try:
                        return query_ref.where("Season", "==", year).limit(5)
                    except:
                        pass
                        
            if match_code:
                try:
                    return query_ref.where("MatchCode", "==", match_code).limit(1)
                except:
                    pass
                    
            if venue:
                venue_fields = ["Venue", "Ground", "Stadium_Name", "Match_Venue"]
                for field in venue_fields:
                    try:
                        return query_ref.where(field, ">=", venue).where(field, "<=", venue + "\uf8ff").limit(5)
                    except:
                        continue
                        
            if opponent:
                opponent_fields = ["Opponent", "Versus", "Against", "Opponent_Team", "Opposing_Team"]
                for field in opponent_fields:
                    try:
                        return query_ref.where(field, ">=", opponent).where(field, "<=", opponent + "\uf8ff").limit(5)
                    except:
                        continue
                        
            if opponent_team:
                opponent_fields = ["Opponent_Team", "Opposing_Team", "Versus", "Against"]
                for field in opponent_fields:
                    try:
                        return query_ref.where(field, ">=", opponent_team).where(field, "<=", opponent_team + "\uf8ff").limit(5)
                    except:
                        continue
                        
            if wicket_position:
                try:
                    return query_ref.where("Wicket_Position", "==", wicket_position).limit(5)
                except:
                    pass
                    
            if runs:
                runs_fields = field_maps.get("runs", ["Runs"]) if field_maps else ["Runs"]
                for field in runs_fields:
                    try:
                        return query_ref.where(field, ">=", int(runs)).limit(5)
                    except:
                        continue
                        
            if season:
                try:
                    return query_ref.where("Season", "==", season).limit(5)
                except:
                    pass
                    
            if margin:
                try:
                    return query_ref.where("Margin", ">=", margin).limit(5)
                except:
                    pass
                    
            if captain_name:
                try:
                    return query_ref.where("Captain_Name", ">=", captain_name).where("Captain_Name", "<=", captain_name + "\uf8ff").limit(5)
                except:
                    pass
                    
            if coach_name:
                try:
                    return query_ref.where("Coach_Name", ">=", coach_name).where("Coach_Name", "<=", coach_name + "\uf8ff").limit(5)
                except:
                    pass
                    
            if auctioneer_name:
                try:
                    return query_ref.where("Auctioneer_Name", ">=", auctioneer_name).where("Auctioneer_Name", "<=", auctioneer_name + "\uf8ff").limit(5)
                except:
                    pass
                    
            if allrounder_name:
                try:
                    return query_ref.where("Allrounder", ">=", allrounder_name).where("Allrounder", "<=", allrounder_name + "\uf8ff").limit(5)
                except:
                    pass
                    
            if umpire_name:
                try:
                    return query_ref.where("Umpire_Name", ">=", umpire_name).where("Umpire_Name", "<=", umpire_name + "\uf8ff").limit(5)
                except:
                    pass
                    
            if innings:
                try:
                    return query_ref.where("Innings", "==", innings).order_by("Runs", direction=firestore.Query.DESCENDING).limit(5)
                except:
                    pass

            # Default ordering based on collection type
            try:
                if collection_name in collection_groups["bowler_records"] or collection_name in collection_groups["bowler_impact"]:
                    return query_ref.order_by("Wickets", direction=firestore.Query.DESCENDING).limit(5)
                elif collection_name in collection_groups["batsman_records"] or collection_name in collection_groups["batsman_milestones"]:
                    return query_ref.order_by("Runs", direction=firestore.Query.DESCENDING).limit(5)
                else:
                    return query_ref.limit(5)
            except Exception as e:
                logger.error(f"Default ordering error: {e}")
                return query_ref.limit(5)
        except Exception as e:
            logger.error(f"Error filtering query: {e}")
            return query_ref.limit(5)

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        team = tracker.get_slot("team")
        team_name = tracker.get_slot("team_name")
        player_name = tracker.get_slot("player_name")
        year = tracker.get_slot("year")
        venue = tracker.get_slot("venue")
        captain_name = tracker.get_slot("captain_name")
        coach_name = tracker.get_slot("coach_name")
        auctioneer_name = tracker.get_slot("auctioneer_name")
        allrounder_name = tracker.get_slot("allrounder_name")
        umpire_name = tracker.get_slot("umpire_name")
        innings = tracker.get_slot("innings")
        season = tracker.get_slot("season")
        opponent_team = tracker.get_slot("opponent_team")
        
        try:
            # Check if this action uses team-specific collections
            if team:
                standardized_team = self.standardize_team_name(team)
                if not standardized_team:
                    dispatcher.utter_message(text="Please specify a team to get their match results.")
                    return []
                try:
                    # First try team match results collections
                    team_short = None
                    for short_name, full_name in team_name_mapping.items():
                        if full_name.lower() == standardized_team.lower() or short_name.lower() == team.lower():
                            team_short = short_name.upper()
                            break
                    
                    if team_short:
                        # Try both formats of team collections
                        collection_name = f"Overall_Match_Results_{team_short}"
                        if collection_name not in all_collections:
                            collection_name = f"{team_short}_with_All"
                    else:
                        collection_name = self.collection_name(standardized_team)
                    
                    query_ref = db.collection(collection_name)
                    query_ref = self.filter_query(query_ref, tracker)
                    
                    results = [self.format_response(doc.to_dict()) for doc in query_ref.stream()]
                    
                    if results:
                        message = f"Here are the results for {standardized_team}:\n\n"
                        # Show first 3 results to avoid overly long messages
                        for i, result in enumerate(results[:3], 1):
                            message += f"{i}. {result}\n"
                        if len(results) > 3:
                            message += f"\n...and {len(results) - 3} more matches."
                        dispatcher.utter_message(text=message)
                    # else:
                    #     dispatcher.utter_message(text=f"Sorry, I couldn't find any matching records for {standardized_team}.")
                except Exception as e:
                    logger.error(f"Error processing team-specific query: {e}")
                    dispatcher.utter_message(text=f"I couldn't retrieve information for {standardized_team}. Please try again.")
            else:
                # Use the standard collection approach for non-team specific collections
                try:
                    collection_name = self.collection_name() if callable(getattr(self, "collection_name")) else self.collection_name
                    query_ref = db.collection(collection_name)
                    query_ref = self.filter_query(query_ref, tracker)
                    
                    results = [self.format_response(doc.to_dict()) for doc in query_ref.stream()]
                    
                    if results:
                        if player_name:
                            dispatcher.utter_message(text=results[0])
                        elif team_name or year or venue or captain_name or coach_name or auctioneer_name or allrounder_name or umpire_name or innings or season or opponent_team:
                            if len(results) == 1:
                                dispatcher.utter_message(text=results[0])
                            else:
                                # Show more data instead of random selection
                                message = "Here are the results I found:\n\n"
                                for i, result in enumerate(results[:3], 1):
                                    message += f"{i}. {result}\n"
                                dispatcher.utter_message(text=message)
                        else:
                            dispatcher.utter_message(text="Sorry, I didn't get that. Can you please rephrase your question")
                except Exception as e:
                    logger.error(f"Error processing standard query: {e}")
                    dispatcher.utter_message(text="I couldn't retrieve the information you're looking for. Please try a different query.")
        except Exception as e:
            logger.error(f"Error retrieving the data: {str(e)}")
            dispatcher.utter_message(text="I encountered an error while processing your request. Please try again.")
            
        return []


# ------------------------------------------------------------------------------------------------------------------------

# Group 1 - Batting stats
class Action_20_to_50_consecutive_innings(FirebaseAction):
    def collection_name(self) -> Text:
        return "20_to_50_Consecutive_Innings"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} scored {doc['Runs']} runs across {doc['Innings']} consecutive IPL innings."

class Action_30_to_50_consecutive_innings(FirebaseAction):
    def collection_name(self) -> Text:
        return "30_to_50_Consecutive_Innings"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} scored {doc['Runs']} runs across {doc['Innings']} consecutive IPL innings."

class Action_40_to_50_consecutive_innings(FirebaseAction):
    def collection_name(self) -> Text:
        return "40_to_50_Consecutive_Innings"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} scored {doc['Runs']} runs across {doc['Innings']} consecutive IPL innings."

class Action_50_on_debut(FirebaseAction):
    def collection_name(self) -> Text:
        return "50_On_Debut"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} scored {doc['Runs']} runs on debut against {doc['Opponent']} at {doc['Venue']}."

class Action_batsman_dismiss_1st_ball(FirebaseAction):
    def collection_name(self) -> Text:
        return "Batsman_Dismiss_1st_Ball_Innings"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Batsman_Name']} was dismissed on the first ball by {doc['Bowler_Name']} at {doc['Venue']}."

class Action_first_50_innings_count(FirebaseAction):
    def collection_name(self) -> Text:
        return "First_50_Innings_Count"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} scored his first IPL fifty in {doc['Innings_to_First_50']} innings."

class Action_highest_strike_rate_innings(FirebaseAction):
    def collection_name(self) -> Text:
        return "highest_strike_rate_innings"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} recorded a strike rate of {doc['Strike_Rate']} against {doc['Opponent']} at {doc['Venue']}."

class Action_innings_to_1st_100(FirebaseAction):
    def collection_name(self) -> Text:
        return "Innings_Take_to_1st_100"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} reached his first century in {doc['Innings']} innings."

class Action_openers_50_and_duck(FirebaseAction):
    def collection_name(self) -> Text:
        return "Openers_50_And_Duck"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player_Pair']} recorded a 50 and a duck against {doc['Opponent']} at {doc['Venue']}."

class Action_opening_pairs_50_partnerships(FirebaseAction):
    def collection_name(self) -> Text:
        return "Opening_Pairs_50_Plus_Partnerships"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player_Pair']} achieved multiple 50+ partnerships."

class Action_scoring_99_an_innings(FirebaseAction):
    def collection_name(self) -> Text:
        return "Scoring_99_an_Innings"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} scored 99 off {doc['Balls_faced']} balls against {doc['Opponent']} at {doc['Venue']}."

class Action_top_scorers_by_position(FirebaseAction):
    def collection_name(self) -> Text:
        return "Top_Scorers_By_Position"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} scored {doc['Number_of_Runs_in_that_Pos']} runs from position {doc['Position_at']}."

class Action_yearwise_highest_averages(FirebaseAction):
    def collection_name(self) -> Text:
        return "Yearwise_Highest_Averages"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} had the highest average of {doc['Average']} in {doc['Year']}."
# ------------------------------------------------------------------------------------------------------------------------

# Group 2 - batting records
class Action_1000_to_8000_runs(FirebaseAction):
    def collection_name(self) -> Text:
        return "1000_to_8000_Runs"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} quickly reached milestones between 1000 and 8000 runs."

class Action_best_strike_rate(FirebaseAction):
    def collection_name(self) -> Text:
        return "Best_Strike_Rate"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} has the best IPL strike rate of {doc['Strike_Rate']}."

class Action_career_partnerships(FirebaseAction):
    def collection_name(self) -> Text:
        return "Career_Partnerships"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} contributed {doc['Partnerships_Runs']} runs in {doc['Number_Unfinished']} career partnerships."

class Action_fastest_centuries(FirebaseAction):
    def collection_name(self) -> Text:
        return "Fastest_Centuries"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} scored a century in just {doc['Balls']} balls against {doc['Opponent']}."

class Action_fastest_fifties(FirebaseAction):
    def collection_name(self) -> Text:
        return "Fastest_Fifties"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} hit a fifty in {doc['Balls']} balls against {doc['Opponent']}."

class Action_fastest_milestone_runs(FirebaseAction):
    def collection_name(self) -> Text:
        return "Fastest_Milestone_Runs"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} reached {doc['Fastest_to_Score']} IPL runs in {doc['Innings']} innings."

class Action_highest_scores_innings(FirebaseAction):
    def collection_name(self) -> Text:
        return "Highest_Scores_Innings"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} scored {doc['Runs']} runs against {doc['Opponent']} at {doc['Venue']}."

class Action_highest_strike_rates_all_time(FirebaseAction):
    def collection_name(self) -> Text:
        return "Highest_Strike_Rates_All_Time"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} maintained a career strike rate of {doc['Strike_Rate']}."

class Action_most_centuries(FirebaseAction):
    def collection_name(self) -> Text:
        return "Most_Centuries"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} has {doc['Hundreds']} centuries with a highest score of {doc['Highest_Score']}."

class Action_most_fifties(FirebaseAction):
    def collection_name(self) -> Text:
        return "Most_Fifties"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} scored {doc['Half_Centuries']} fifties and {doc['Centuries']} centuries, totaling {doc['Runs']} runs."

class Action_most_runs_2008_2024(FirebaseAction):
    def collection_name(self) -> Text:
        return "Most_Runs_2008_2024"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} scored {doc['Runs']} runs between 2008 and 2024."

class Action_most_runs_from_boundaries(FirebaseAction):
    def collection_name(self) -> Text:
        return "Most_Runs_From_Boundaries_Per_Innings"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} scored {doc['Boundary_Runs']} boundary runs hitting {doc['Fours']} fours and {doc['Sixes']} sixes."

class Action_most_runs_overall(FirebaseAction):
    def collection_name(self) -> Text:
        return "Most_Runs_Overall"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} scored {doc['Runs']} runs in IPL with {doc['Centuries']} centuries and {doc['Fifties']} fifties."

class Action_most_sixes_2008_2024(FirebaseAction):
    def collection_name(self) -> Text:
        return "Most_Sixes_2008_2024"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} hit {doc['Sixes']} sixes between 2008 and 2024."

class Action_most_sixes_all_time(FirebaseAction):
    def collection_name(self) -> Text:
        return "Most_Sixes_All_Times"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} smashed {doc['Sixes']} sixes in IPL history."

# ------------------------------------------------------------------------------------------------------------------------

# Group 3  - Player Impact
class action_player_impact_by_season(Action):
    def name(self) -> Text:
        return "action_player_impact_by_season"

    def get_collection_for_season_range(self, season_range: str) -> str:
        if season_range == "2008-2010":
            return "Player_Impact_2008_2010"
        elif season_range == "2011-2013":
            return "Player_Impact_2011_2013"
        elif season_range == "2014-2016":
            return "Player_Impact_2014_2016"
        elif season_range == "2017-2019":
            return "Player_Impact_2017_2019"
        elif season_range == "2020-2022":
            return "Player_Impact_2020_2022"
        elif season_range == "2023-2024":
            return "Player_Impact_2023_2024"
        
        # Default to most recent
        return "Player_Impact_2023_2024"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        player_name = tracker.get_slot("player_name")
        team_name = tracker.get_slot("team_name")
        year = tracker.get_slot("year")
        season_range = tracker.get_slot("season_range")
        
        if not season_range and year:
            # Convert single year to appropriate range
            if "2008" <= year <= "2010":
                season_range = "2008-2010"
            elif "2011" <= year <= "2013":
                season_range = "2011-2013"
            elif "2014" <= year <= "2016":
                season_range = "2014-2016"
            elif "2017" <= year <= "2019":
                season_range = "2017-2019"
            elif "2020" <= year <= "2022":
                season_range = "2020-2022"
            elif "2023" <= year <= "2024":
                season_range = "2023-2024"
            else:
                season_range = "2023-2024"  # Default to latest

        collection_name = self.get_collection_for_season_range(season_range)
        query_ref = db.collection(collection_name)

        # Apply filters based on slots
        if player_name:
            query_ref = query_ref.where("Player", ">=", player_name).where("Player", "<=", player_name + "\uf8ff")
        if team_name:
            query_ref = query_ref.where("Team", ">=", team_name).where("Team", "<=", team_name + "\uf8ff")
        if year and not season_range:
            query_ref = query_ref.where("Season", "==", year)

        # Order by runs (descending) by default
        query_ref = query_ref.order_by("Runs", direction=firestore.Query.DESCENDING).limit(5)
        results = []

        for doc in query_ref.stream():
            player_data = doc.to_dict()
            results.append(f"{player_data['Player']} from {player_data['Team']} scored {player_data['Runs']} runs in {player_data['Season']} with an average of {player_data['Average']} and strike rate of {player_data['Strike_Rate']}. They contributed {player_data['Team_Runs_Percentage']} of their team's total runs.")

        if results:
            if player_name:
                dispatcher.utter_message(text=results[0])
            else:
                dispatcher.utter_message(text=random.choice(results))
        else:
            dispatcher.utter_message(text="Sorry, I didn't get that. Can you please rephrase your question")
        
        return []

class action_wicketkeeper_highest_scores(FirebaseAction):
    def collection_name(self) -> Text:
        return "Wicketkeeper_Highest_Scores"

    def filter_query(self, query_ref, tracker: Tracker):
        player_name = tracker.get_slot("player_name")
        opponent_team = tracker.get_slot("opponent_team")
        venue = tracker.get_slot("venue")

        if player_name:
            query_ref = query_ref.where("Player", ">=", player_name).where("Player", "<=", player_name + "\uf8ff")
        if opponent_team:
            query_ref = query_ref.where("Opponent_Team", ">=", opponent_team).where("Opponent_Team", "<=", opponent_team + "\uf8ff")
        if venue:
            query_ref = query_ref.where("Match_Venue", ">=", venue).where("Match_Venue", "<=", venue + "\uf8ff")

        return query_ref.order_by("Runs", direction=firestore.Query.DESCENDING).limit(5)

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} scored {doc['Runs']} runs off {doc['Balls_Faced']} balls (SR: {doc['Strike_Rate']}) against {doc['Opponent_Team']} at {doc['Match_Venue']} on {doc['Date']}."

class action_wicketkeeper_most_dismissals_innings(FirebaseAction):
    def collection_name(self) -> Text:
        return "Wicketkeeper_Most_Dismissals_Per_Innings"

    def filter_query(self, query_ref, tracker: Tracker):
        player_name = tracker.get_slot("player_name")
        team_name = tracker.get_slot("team_name")
        opponent_team = tracker.get_slot("opponent_team")
        venue = tracker.get_slot("venue")

        if player_name:
            query_ref = query_ref.where("Player", ">=", player_name).where("Player", "<=", player_name + "\uf8ff")
        if team_name:
            query_ref = query_ref.where("Team(s)", ">=", team_name).where("Team(s)", "<=", team_name + "\uf8ff")
        if opponent_team:
            query_ref = query_ref.where("Opponent_Team", ">=", opponent_team).where("Opponent_Team", "<=", opponent_team + "\uf8ff")
        if venue:
            query_ref = query_ref.where("Match_Venue", ">=", venue).where("Match_Venue", "<=", venue + "\uf8ff")

        return query_ref.order_by("Total_Dismissals", direction=firestore.Query.DESCENDING).limit(5)

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} of {doc['Team(s)']} had {doc['Total_Dismissals']} dismissals ({doc['Catches']} catches and {doc['Stumpings']} stumpings) against {doc['Opponent_Team']} at {doc['Match_Venue']} on {doc['Date']}."

class action_wicketkeeper_overall_records(FirebaseAction):
    def collection_name(self) -> Text:
        return "Wicketkeeper_Overall_Records_with_Stumpings"

    def filter_query(self, query_ref, tracker: Tracker):
        player_name = tracker.get_slot("player_name")
        team_name = tracker.get_slot("team_name")

        if player_name:
            query_ref = query_ref.where("Player", ">=", player_name).where("Player", "<=", player_name + "\uf8ff")
        if team_name:
            query_ref = query_ref.where("Teams_Represented", ">=", team_name).where("Teams_Represented", "<=", team_name + "\uf8ff")

        return query_ref.order_by("Dismissals", direction=firestore.Query.DESCENDING).limit(5)

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} ({doc['Teams_Represented']}) has {doc['Dismissals']} total dismissals ({doc['Catches']} catches and {doc['Stumpings']} stumpings) in {doc['Match']} matches, averaging {doc['Dismissals_Per_Match']} dismissals per match. With the bat, they've scored {doc['Runs']} runs at an average of {doc['Average']}."

# ------------------------------------------------------------------------------------------------------------------------

# Group 4  - Bowling stats
class action_bowler_impact_by_year(Action):
    def name(self) -> Text:
        return "action_bowler_impact_by_year"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        year = tracker.get_slot("year")
        player_name = tracker.get_slot("player_name")
        team_name = tracker.get_slot("team_name")

        # Determine which collection to query based on the year
        if year:
            year_int = int(year)
            if 2008 <= year_int <= 2012:
                collection_name = "2008_2012_Bowler_Impact"
            elif 2013 <= year_int <= 2016:
                collection_name = "2013_2016_Bowler_Impact"
            elif 2017 <= year_int <= 2021:
                collection_name = "2017_2021_Bowler_Impact"
            elif 2022 <= year_int <= 2024:
                collection_name = "2022_2024_Bowler_Impact"
            else:
                dispatcher.utter_message(text="Sorry, I didn't get that. Can you please rephrase your question")
                return []
        else:
            # Default to the most recent data if no year specified
            collection_name = "2022_2024_Bowler_Impact"

        query_ref = db.collection(collection_name)
        
        if player_name:
            query_ref = query_ref.where("Player", ">=", player_name).where("Player", "<=", player_name + "\uf8ff").limit(1)
        elif team_name:
            query_ref = query_ref.where("Team", ">=", team_name).where("Team", "<=", team_name + "\uf8ff").limit(5)
        elif year:
            query_ref = query_ref.where("Season", "==", year).order_by("Wickets", direction=firestore.Query.DESCENDING).limit(5)
        else:
            query_ref = query_ref.order_by("Wickets", direction=firestore.Query.DESCENDING).limit(5)

        docs = query_ref.stream()
        results = []

        for doc in docs:
            data = doc.to_dict()
            results.append(f"{data['Player']} from {data['Team']} took {data['Wickets']} wickets in {data['Matches']} matches with an economy rate of {data['Economy_Rate']} in the {data['Season']} season.")

        if results:
            if player_name:
                dispatcher.utter_message(text=results[0])
            else:
                dispatcher.utter_message(text=random.choice(results))
        else:
            dispatcher.utter_message(text="Sorry, I didn't get that. Can you please rephrase your question")
        
        return []

class action_most_4_wickets_innings(FirebaseAction):
    def collection_name(self) -> Text:
        return "Most_4_Wickets_Innings"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} has taken 4 or more wickets in {doc['4_Wickets_Matches']} matches, with a best figure of {doc['Best_Figures']} while playing for {doc['Teams']}."

class action_most_economical(FirebaseAction):
    def collection_name(self) -> Text:
        return "Most_Economical"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} is one of the most economical bowlers with an economy rate of {doc['Economy_Rate']}, taking {doc['Wickets']} wickets in {doc['Matches']} matches while playing for {doc['Team(s)']}."

class action_most_wickets_1st_50_matches(FirebaseAction):
    def collection_name(self) -> Text:
        return "Most_Wickets_1st_50_Matches"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player_Name']} took {doc['First_50_Wickets']} wickets in their first 50 matches with an average of {doc['First_50_Average']} and a strike rate of {doc['First_50_Strike_Rate']}."

class action_most_wickets_consecutive_matches(FirebaseAction):
    def collection_name(self) -> Text:
        return "Most_Wickets_Consecutive_Matches"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player_Name']} took {doc['Consecutive_Wickets']} wickets in {doc['Consecutive_Matches']} consecutive matches with an average of {doc['Consecutive_Average']} and a strike rate of {doc['Consecutive_StrikeRate']}."

class action_most_wickets_in_ipl(FirebaseAction):
    def collection_name(self) -> Text:
        return "Most_Wickets_in_IPL"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} has taken {doc['Wickets']} wickets in {doc['Matches']} matches with an average of {doc['Bowling_Average']} and best bowling figures of {doc['Best_Bowling']} while playing for {doc['Teams']}."

class action_most_wickets_innings(FirebaseAction):
    def collection_name(self) -> Text:
        return "Most_Wickets_Innings"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Bowler']} from {doc['Bowler_Team']} took {doc['Wickets']} wickets in {doc['Overs']} overs against {doc['Opponent_Team']} at {doc['Match_Venue']} on {doc['Match_Date']}, conceding just {doc['Runs']} runs."

# ------------------------------------------------------------------------------------------------------------------------

# Group 5 - Bowling records
class Action_best_economy_rates_innings(FirebaseAction):
    def collection_name(self) -> Text:
        return "Best_Economy_Rates_Innings"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Bowler']} from {doc['Team_Name']} had an economy rate of {doc['Economy_Rate']} against {doc['Opponent']} at {doc['Venue']}."

class Action_bowler_best_strike_rate(FirebaseAction):
    def collection_name(self) -> Text:
        return "Bowler_Best_Strike_Rate"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} has a strike rate of {doc['Strike_Rate']} with {doc['Wickets']} wickets."

class Action_bowler_dismissal_records(FirebaseAction):
    def collection_name(self) -> Text:
        return "Bowler_Dismissal_Records"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Bowler']} dismissed {doc['Batsman']} in {doc['Innings_Faced']} innings, with a dismissal percentage of {doc['Dismissal_Percentage']}."

class Action_fastest_player_50_wickets(FirebaseAction):
    def collection_name(self) -> Text:
        return "Fastest_Player_50_Wickets"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} took {doc['Matches']} matches to reach {doc['Wickets']} wickets with an average of {doc['Average']}."

class Action_first_ball_wicket(FirebaseAction):
    def collection_name(self) -> Text:
        return "First_Ball_Wicket"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} took a first-ball wicket against {doc['Dismissed_Batsman']} at {doc['Venue']}."

class Action_ipl_bowlers_data_2008_2024(FirebaseAction):
    def collection_name(self) -> Text:
        return "IPL_Bowlers_Data_2008_2024"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} from {doc['Team']} has {doc['Wickets']} wickets in {doc['Matches']} matches with an economy rate of {doc['Economy']}."

class Action_ipl_hat_tricks(FirebaseAction):
    def collection_name(self) -> Text:
        return "IPL_Hat_Tricks"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Bowler']} took a hat-trick dismissing {doc['Dismissed_Batsmen']} in a match against {doc['Opponent_Team']} at {doc['Match_Venue']}."

class Action_lowest_averages(FirebaseAction):
    def collection_name(self) -> Text:
        return "Lowest_Averages"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} has the lowest bowling average of {doc['Average']} in IPL."

class Action_most_runs_conceded(FirebaseAction):
    def collection_name(self) -> Text:
        return "Most_Runs_Conceded"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} conceded {doc['Runs']} runs in {doc['Overs']} overs against {doc['Opponent']} at {doc['Venue']}."

# ------------------------------------------------------------------------------------------------------------------------

# Group 6 - Overall statistics
class Action_all_players_records(FirebaseAction):
    def collection_name(self) -> Text:
        return "All_Players_Records"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Name']} has played for {doc['Team(s)']} in {doc['Matches']} matches, scoring {doc['Runs']} runs with a batting average of {doc['Batting_Average']} and taking {doc['Wickets']} wickets with a bowling average of {doc['Bowling_Average']}."

class Action_auctioneers(FirebaseAction):
    def collection_name(self) -> Text:
        return "Auctioneers"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"In {doc['Year']}, the IPL auction was conducted by {doc['Auctioneer_Name']}."

class Action_cap_holders(FirebaseAction):
    def collection_name(self) -> Text:
        return "Cap_Holders"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"In IPL {doc['Year']}, {doc['Orange_Cap_Holder']} from {doc['Orange_Cap_Team']} won the Orange Cap scoring {doc['Runs']} runs with highest score of {doc['Highest_Score']}, while {doc['Purple_Cap_Holder']} from {doc['Purple_Cap_Team']} won the Purple Cap taking {doc['Wickets']} wickets with best bowling figure of {doc['Best_Bowling_Figure']}."

class Action_coaches_overall(FirebaseAction):
    def collection_name(self) -> Text:
        return "Coaches_Overrall"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        coaches_info = []
        for team, coach in doc.items():
            if team != "Year" and coach != "NA":
                coaches_info.append(f"{team}: {coach}")
        
        coaches_text = ", ".join(coaches_info)
        return f"In {doc['Year']}, the coaches were: {coaches_text}."

class Action_grounds_records(FirebaseAction):
    def collection_name(self) -> Text:
        return "Grounds_Records"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Stadium_Name']} located in {doc['City_Name']}, {doc['Country_Name']} has hosted {doc['Total_Matches']} IPL matches."

class Action_highest_catches(FirebaseAction):
    def collection_name(self) -> Text:
        return "Highest_Catches"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} who played for {doc['Team(s)']} has taken {doc['Catches']} catches in {doc['Matches']} matches with maximum {doc['Most_Catches_in_1_Match']} catches in a single match."

class Action_ipl_captains_records(FirebaseAction):
    def collection_name(self) -> Text:
        return "IPL_Captains_Records"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} has captained {doc['Teams_Captained_List']} for {doc['Matches']} matches with {doc['Matches_Won']} wins, {doc['Matches_Lost']} losses, {doc['Matches_No_Result']} no results, and a toss win percentage of {doc['Toss_Win_Percentage']}."

class Action_ipl_players_overall_data(FirebaseAction):
    def collection_name(self) -> Text:
        return "IPL_Players_Overall_Data_2008_2024"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} played for {doc['Team']} in {doc['Year']}, scoring {doc['Runs']} runs in {doc['Innings']} innings with {doc['Fifties']} fifties, {doc['Hundreds']} hundreds at a strike rate of {doc['Strike_Rate']} and average of {doc['Average']}. They contributed to {doc['Team_Runs_Percentage']} of their team's total runs."

class Action_ipl_team_captains_records(FirebaseAction):
    def collection_name(self) -> Text:
        return "IPL_Team_Captains_Overall_Records"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Captain_Name']} as captain of {doc['Team']} led in {doc['Matches']} matches with {doc['Won']} wins, {doc['Lost']} losses, {doc['No_Result']} no results, and a toss win percentage of {doc['Toss_Wins_Percentage']}."

class Action_most_catch_in_an_innings(FirebaseAction):
    def collection_name(self) -> Text:
        return "Most_Catch_in_an_Innings"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} from {doc['Team']} took {doc['Catches']} catches against {doc['Versus']} at {doc['Ground']} on {doc['Date']}."

class Action_most_ducks_in_career(FirebaseAction):
    def collection_name(self) -> Text:
        return "Most_Ducks_In_Career"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Player']} has recorded {doc['Ducks']} ducks in {doc['Innings']} innings. They have played for {doc['Teams']} and scored {doc['Runs']} runs at an average of {doc['Average']} and strike rate of {doc['Strike_Rate']}."

class Action_tied_matches(FirebaseAction):
    def collection_name(self) -> Text:
        return "Tied_Matches"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"The match between {doc['Teams_Competing']} at {doc['Match_Venue']} on {doc['Match_Date']} ended in a tie. {doc['Match_Result']}."

class Action_top_allrounders(FirebaseAction):
    def collection_name(self) -> Text:
        return "Top_Allrounders"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Allrounder']} who played for {doc['Team_Names']} has scored {doc['Total_Runs']} runs at an average of {doc['Batting_Average']} and taken {doc['Total_Wickets']} wickets at an average of {doc['Bowling_Average']} in {doc['Total_Matches']} matches."

class Action_umpire_data(FirebaseAction):
    def collection_name(self) -> Text:
        return "Umpire_Data"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Umpire_Name']} has officiated in {doc['Matches']} IPL matches from {doc['Span']}."

# ------------------------------------------------------------------------------------------------------------------------

# Group 7 - Overall Match Results
class Action_team_matches(FirebaseAction):
    def collection_name(self) -> Text:
        return "Team_Matches"
        
    def filter_query(self, query_ref, tracker: Tracker):
        team = tracker.get_slot("team")
        if team:
            # For team matches, we simply limit to most recent matches
            return query_ref.order_by("Season", direction=firestore.Query.DESCENDING).limit(10)
        return query_ref.limit(10)

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Season']} - {doc['Match']} - {doc['Team']} vs {doc['Versus']} at {doc['Venue']} - {doc['Result']}"

class Action_team_performance_against_opponent(FirebaseAction):
    def collection_name(self) -> Text:
        return "Team_Performance_Against_Opponent"
        
    def filter_query(self, query_ref, tracker: Tracker):
        opponent = tracker.get_slot("opponent")
        standardized_opponent = self.standardize_team_name(opponent)
        
        if standardized_opponent:
            return query_ref.where("Versus", "==", standardized_opponent).limit(10)
        return query_ref.limit(10)

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Season']} - {doc['Team']} vs {doc['Versus']} - {doc['Result']}"

class Action_team_performance_at_venue(FirebaseAction):
    def collection_name(self) -> Text:
        return "Team_Performance_At_Venue"
        
    def filter_query(self, query_ref, tracker: Tracker):
        venue = tracker.get_slot("venue")
        if venue:
            return query_ref.where("Venue", ">=", venue).where("Venue", "<=", venue + "\uf8ff").limit(10)
        return query_ref.limit(10)

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Season']} - {doc['Team']} vs {doc['Versus']} at {doc['Venue']} - {doc['Result']}"

class Action_team_season_performance(FirebaseAction):
    def collection_name(self) -> Text:
        return "Team_Season_Performance"
        
    def filter_query(self, query_ref, tracker: Tracker):
        season = tracker.get_slot("season")
        if season:
            return query_ref.where("Season", "==", season).limit(20)
        return query_ref.limit(10)

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Season']} - {doc['Match']} - {doc['Team']} vs {doc['Versus']} - {doc['Result']}"

class Action_team_win_percentage(FirebaseAction):
    def collection_name(self) -> Text:
        return "Team_Win_Percentage"
        
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        team = tracker.get_slot("team")
        standardized_team = self.standardize_team_name(team)
        
        if not standardized_team:
            dispatcher.utter_message(text="Please specify a team to calculate their win percentage.")
            return []
            
        collection = self.collection_name()
        query_ref = db.collection(collection)
        
        try:
            docs = list(query_ref.stream())
            total_matches = len(docs)
            
            if total_matches == 0:
                dispatcher.utter_message(text="Sorry, I didn't get that. Can you please rephrase your question")
                return []
                
            wins = 0
            for doc in docs:
                result = doc.to_dict().get("Result", "")
                if standardized_team in result and "won" in result:
                    wins += 1
                    
            win_percentage = (wins / total_matches) * 100
            
            dispatcher.utter_message(text=f"{standardized_team} has won {wins} out of {total_matches} matches, with a win percentage of {win_percentage:.2f}%.")
        except Exception as e:
            dispatcher.utter_message(text="Sorry, I didn't get that. Can you please rephrase your question")
        
        return []

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        # Not used in this action since we override run()
        pass

class Action_head_to_head(FirebaseAction):
    def collection_name(self) -> Text:
        return "Head_To_Head"
        
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        team = tracker.get_slot("team")
        opponent = tracker.get_slot("opponent")
        
        standardized_team = self.standardize_team_name(team)
        standardized_opponent = self.standardize_team_name(opponent)
        
        if not standardized_team or not standardized_opponent:
            dispatcher.utter_message(text="Sorry, I didn't get that. Can you please rephrase your question")
            return []
            
        collection = self.collection_name()
        query_ref = db.collection(collection)
        
        try:
            # Get matches between these two teams
            query_ref = query_ref.where("Team", "==", standardized_team).where("Versus", "==", standardized_opponent)
            docs = list(query_ref.stream())
            
            if not docs:
                dispatcher.utter_message(text="Sorry, I didn't get that. Can you please rephrase your question")
                return []
                
            total_matches = len(docs)
            team_wins = 0
            opponent_wins = 0
            
            for doc in docs:
                result = doc.to_dict().get("Result", "")
                if standardized_team in result and "won" in result:
                    team_wins += 1
                elif standardized_opponent in result and "won" in result:
                    opponent_wins += 1
                    
            message = f"Head-to-head: {standardized_team} vs {standardized_opponent}\n"
            message += f"Total matches: {total_matches}\n"
            message += f"{standardized_team} wins: {team_wins}\n"
            message += f"{standardized_opponent} wins: {opponent_wins}\n"
            
            if total_matches - team_wins - opponent_wins > 0:
                message += f"No result/Tied: {total_matches - team_wins - opponent_wins}"
                
            dispatcher.utter_message(text=message)
        except Exception as e:
            dispatcher.utter_message(text="Sorry, I didn't get that. Can you please rephrase your question")
        
        return []

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        # Not used in this action since we override run()
        pass

class Action_most_successful_team(Action):
    def name(self) -> Text:
        return "action_most_successful_team"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # This would require querying across multiple collections for all teams
        # For demonstration, we'll provide a hardcoded response
        dispatcher.utter_message(text="Based on IPL history, Mumbai Indians is the most successful team with 5 IPL titles, followed by Chennai Super Kings with 4 titles.")
        return []

class Action_team_results_by_year(FirebaseAction):
    def collection_name(self) -> Text:
        return "Team_Results_By_Year"
        
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        team = tracker.get_slot("team")
        standardized_team = self.standardize_team_name(team)
        
        if not standardized_team:
            dispatcher.utter_message(text="Please specify a team to get their year-by-year results.")
            return []
            
        collection = self.collection_name()
        query_ref = db.collection(collection)
        
        try:
            query_ref = query_ref.where("Team", "==", standardized_team)
            docs = list(query_ref.stream())
            if not docs:
                dispatcher.utter_message(text="Sorry, I didn't get that. Can you please rephrase your question")
                return []
                
            # Group matches by season
            seasons = {}
            for doc in docs:
                data = doc.to_dict()
                season = data.get("Season", "Unknown")
                result = data.get("Result", "")
                
                if season not in seasons:
                    seasons[season] = {"total": 0, "wins": 0}
                
                seasons[season]["total"] += 1
                if standardized_team in result and "won" in result:
                    seasons[season]["wins"] += 1
            
            message = f"Year-by-year performance for {standardized_team}:\n\n"
            for season in sorted(seasons.keys()):
                win_percentage = (seasons[season]["wins"] / seasons[season]["total"]) * 100
                message += f"{season}: {seasons[season]['wins']} wins out of {seasons[season]['total']} matches ({win_percentage:.1f}%)\n"
                
            dispatcher.utter_message(text=message)
        except Exception as e:
            dispatcher.utter_message(text="Sorry, I didn't get that. Can you please rephrase your question")
        
        return []

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        # Not used in this action since we override run()
        pass

class Action_team_home_away_performance(FirebaseAction):
    def collection_name(self) -> Text:
        return "Team_Home_Away_Performance"
        
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        team = tracker.get_slot("team")
        standardized_team = self.standardize_team_name(team)
        
        if not standardized_team:
            dispatcher.utter_message(text="Please specify a team to get their home vs away performance.")
            return []
            
        collection = self.collection_name()
        query_ref = db.collection(collection)
        
        try:
            query_ref = query_ref.where("Team", "==", standardized_team)
            docs = list(query_ref.stream())
            
            if not docs:
                dispatcher.utter_message(text="Sorry, I didn't get that. Can you please rephrase your question")
                return []
                
            # Determine home venues for each team (simplified approach)
            home_venues = {
                "Chennai Super Kings": ["MA Chidambaram Stadium"],
                "Mumbai Indians": ["Wankhede Stadium"],
                "Royal Challengers Bengaluru": ["M Chinnaswamy Stadium"],
                "Kolkata Knight Riders": ["Eden Gardens"],
                "Delhi Capitals": ["Arun Jaitley Stadium", "Feroz Shah Kotla"],
                "Sunrisers Hyderabad": ["Rajiv Gandhi International Stadium"],
                "Rajasthan Royals": ["Sawai Mansingh Stadium"],
                "Punjab Kings": ["Punjab Cricket Association IS Bindra Stadium", "Mohali"],
                "Gujarat Titans": ["Narendra Modi Stadium"],
                "Lucknow Super Giants": ["Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium"]
            }
            
            team_home_venues = home_venues.get(standardized_team, [])
            
            home_matches = {"total": 0, "wins": 0}
            away_matches = {"total": 0, "wins": 0}
            
            for doc in docs:
                data = doc.to_dict()
                venue = data.get("Venue", "")
                result = data.get("Result", "")
                
                is_home_match = any(home_venue in venue for home_venue in team_home_venues)
                
                if is_home_match:
                    home_matches["total"] += 1
                    if standardized_team in result and "won" in result:
                        home_matches["wins"] += 1
                else:
                    away_matches["total"] += 1
                    if standardized_team in result and "won" in result:
                        away_matches["wins"] += 1
            
            home_win_pct = (home_matches["wins"] / home_matches["total"] * 100) if home_matches["total"] > 0 else 0
            away_win_pct = (away_matches["wins"] / away_matches["total"] * 100) if away_matches["total"] > 0 else 0
            
            message = f"Home vs Away performance for {standardized_team}:\n\n"
            message += f"Home: {home_matches['wins']} wins out of {home_matches['total']} matches ({home_win_pct:.1f}%)\n"
            message += f"Away: {away_matches['wins']} wins out of {away_matches['total']} matches ({away_win_pct:.1f}%)"
            
            dispatcher.utter_message(text=message)
        except Exception as e:
            dispatcher.utter_message(text="Sorry, I didn't get that. Can you please rephrase your question")
        
        return []

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        # Not used in this action since we override run()
        pass

# ------------------------------------------------------------------------------------------------------------------------

class action_team_ground_performance(FirebaseAction):
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        team = tracker.get_slot("team")
        ground = tracker.get_slot("ground")
        
        standardized_team = self.standardize_team_name(team)
        standardized_ground = self.standardize_ground_name(ground)
        
        if not standardized_team:
            dispatcher.utter_message(text="Please specify a team to check their performance at a ground.")
            return []
            
        if not standardized_ground:
            dispatcher.utter_message(text="Please specify a ground to check the team's performance there.")
            return []
            
        collection = self.collection_name(standardized_team)
        query_ref = db.collection(collection)
        
        try:
            results = []
            # Find documents where Ground matches the specified ground
            for doc in query_ref.stream():
                data = doc.to_dict()
                if standardized_ground.lower() in data.get("Ground", "").lower():
                    results.append(data)
            
            if not results:
                dispatcher.utter_message(text="Sorry, I didn't get that. Can you please rephrase your question")
                return []
                
            total_wins = 0
            total_losses = 0
            total_no_results = 0
            total_matches = 0
            
            for result in results:
                team_wins = int(result.get(standardized_team, "0"))
                opponent_wins = int(result.get("Opponent", "0"))
                no_results = int(result.get("No Result", "0"))
                
                total_wins += team_wins
                total_losses += opponent_wins
                total_no_results += no_results
                total_matches += int(result.get("Total", "0"))
            
            message = f"{standardized_team} at {standardized_ground}:\n"
            message += f"Wins: {total_wins}\n"
            message += f"Losses: {total_losses}\n"
            message += f"No Results: {total_no_results}\n"
            message += f"Total Matches: {total_matches}\n"
            win_percentage = (total_wins / (total_matches - total_no_results)) * 100 if (total_matches - total_no_results) > 0 else 0
            message += f"Win Percentage: {win_percentage:.2f}%"
            
            dispatcher.utter_message(text=message)
        except Exception as e:
            dispatcher.utter_message(text="Sorry, I didn't get that. Can you please rephrase your question")
        
        return []


class action_team_opponent_record(FirebaseAction):
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        team = tracker.get_slot("team")
        opponent = tracker.get_slot("opponent")
        
        standardized_team = self.standardize_team_name(team)
        standardized_opponent = self.standardize_team_name(opponent)
        
        if not standardized_team:
            dispatcher.utter_message(text="Please specify a team to check their record against an opponent.")
            return []
            
        if not standardized_opponent:
            dispatcher.utter_message(text="Please specify an opponent team to check the record against.")
            return []
            
        collection = self.collection_name(standardized_team)
        query_ref = db.collection(collection)
        
        try:
            results = []
            # Find documents where Against matches the specified opponent
            for doc in query_ref.stream():
                data = doc.to_dict()
                if standardized_opponent.lower() in data.get("Against", "").lower():
                    results.append(data)
            
            if not results:
                dispatcher.utter_message(text=f"I couldn't find any matches between {standardized_team} and {standardized_opponent}.")
                return []
                
            total_wins = 0
            total_losses = 0
            total_no_results = 0
            total_matches = 0
            
            for result in results:
                team_wins = int(result.get(standardized_team, "0"))
                opponent_wins = int(result.get("Opponent", "0"))
                no_results = int(result.get("No Result", "0"))
                
                total_wins += team_wins
                total_losses += opponent_wins
                total_no_results += no_results
                total_matches += int(result.get("Total", "0"))
            
            message = f"{standardized_team} vs {standardized_opponent}:\n"
            message += f"{standardized_team} wins: {total_wins}\n"
            message += f"{standardized_opponent} wins: {total_losses}\n"
            message += f"No Results: {total_no_results}\n"
            message += f"Total Matches: {total_matches}\n"
            win_percentage = (total_wins / (total_matches - total_no_results)) * 100 if (total_matches - total_no_results) > 0 else 0
            message += f"Win Percentage: {win_percentage:.2f}%"
            
            dispatcher.utter_message(text=message)
        except Exception as e:
            dispatcher.utter_message(text=f"Error retrieving team vs opponent data: {str(e)}")
        
        return []


class action_team_overall_record(FirebaseAction):
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        team = tracker.get_slot("team")
        standardized_team = self.standardize_team_name(team)
        
        if not standardized_team:
            dispatcher.utter_message(text="Please specify a team to check their overall record.")
            return []
            
        collection = self.collection_name(standardized_team)
        query_ref = db.collection(collection)
        
        try:
            total_wins = 0
            total_losses = 0
            total_no_results = 0
            total_matches = 0
            
            for doc in query_ref.stream():
                data = doc.to_dict()
                team_wins = int(data.get(standardized_team, "0"))
                opponent_wins = int(data.get("Opponent", "0"))
                no_results = int(data.get("No Result", "0"))
                
                total_wins += team_wins
                total_losses += opponent_wins
                total_no_results += no_results
                total_matches += int(data.get("Total", "0"))
            
            if total_matches == 0:
                dispatcher.utter_message(text=f"I couldn't find any match records for {standardized_team}.")
                return []
            
            message = f"Overall record for {standardized_team}:\n"
            message += f"Wins: {total_wins}\n"
            message += f"Losses: {total_losses}\n"
            message += f"No Results: {total_no_results}\n"
            message += f"Total Matches: {total_matches}\n"
            win_percentage = (total_wins / (total_matches - total_no_results)) * 100 if (total_matches - total_no_results) > 0 else 0
            message += f"Win Percentage: {win_percentage:.2f}%"
            
            dispatcher.utter_message(text=message)
        except Exception as e:
            dispatcher.utter_message(text=f"Error retrieving overall team data: {str(e)}")
        
        return []


class action_team_home_ground_record(FirebaseAction):
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        team = tracker.get_slot("team")
        standardized_team = self.standardize_team_name(team)
        
        if not standardized_team:
            dispatcher.utter_message(text="Please specify a team to check their home ground record.")
            return []
        
        # Map teams to their home grounds
        home_grounds = {
            "Chennai Super Kings": ["MA Chidambaram Stadium"],
            "Mumbai Indians": ["Wankhede Stadium"],
            "Royal Challengers Bengaluru": ["M Chinnaswamy Stadium"],
            "Kolkata Knight Riders": ["Eden Gardens"],
            "Delhi Capitals": ["Arun Jaitley Stadium", "Feroz Shah Kotla"],
            "Sunrisers Hyderabad": ["Rajiv Gandhi International Stadium"],
            "Rajasthan Royals": ["Sawai Mansingh Stadium"],
            "Punjab Kings": ["Punjab Cricket Association IS Bindra Stadium", "Mohali"],
            "Gujarat Titans": ["Narendra Modi Stadium"],
            "Lucknow Super Giants": ["Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium"]
        }
        
        team_home_grounds = home_grounds.get(standardized_team, [])
        if not team_home_grounds:
            dispatcher.utter_message(text=f"Sorry, I don't know the home ground for {standardized_team}.")
            return []
            
        collection = self.collection_name(standardized_team)
        query_ref = db.collection(collection)
        
        try:
            results = []
            # Find documents where Ground matches any of the team's home grounds
            for doc in query_ref.stream():
                data = doc.to_dict()
                ground = data.get("Ground", "")
                if any(home_ground.lower() in ground.lower() for home_ground in team_home_grounds):
                    results.append(data)
            
            if not results:
                dispatcher.utter_message(text="Sorry, I didn't get that. Can you please rephrase your question")
                return []
                
            total_wins = 0
            total_losses = 0
            total_no_results = 0
            total_matches = 0
            
            for result in results:
                team_wins = int(result.get(standardized_team, "0"))
                opponent_wins = int(result.get("Opponent", "0"))
                no_results = int(result.get("No Result", "0"))
                
                total_wins += team_wins
                total_losses += opponent_wins
                total_no_results += no_results
                total_matches += int(result.get("Total", "0"))
            
            message = f"{standardized_team} home record:\n"
            message += f"Wins: {total_wins}\n"
            message += f"Losses: {total_losses}\n"
            message += f"No Results: {total_no_results}\n"
            message += f"Total Matches: {total_matches}\n"
            win_percentage = (total_wins / (total_matches - total_no_results)) * 100 if (total_matches - total_no_results) > 0 else 0
            message += f"Home Win Percentage: {win_percentage:.2f}%"
            
            dispatcher.utter_message(text=message)
        except Exception as e:
            dispatcher.utter_message(text=f"Error retrieving home ground data: {str(e)}")
        
        return []


class action_team_performance_by_opponent(FirebaseAction):
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        team = tracker.get_slot("team")
        standardized_team = self.standardize_team_name(team)
        
        if not standardized_team:
            dispatcher.utter_message(text="Please specify a team to check their performance against all opponents.")
            return []
            
        collection = self.collection_name(standardized_team)
        query_ref = db.collection(collection)
        
        try:
            # Group results by opponent
            opponent_stats = {}
            
            for doc in query_ref.stream():
                data = doc.to_dict()
                opponent = data.get("Against", "")
                
                if opponent not in opponent_stats:
                    opponent_stats[opponent] = {
                        "wins": 0,
                        "losses": 0,
                        "no_results": 0,
                        "total": 0
                    }
                
                opponent_stats[opponent]["wins"] += int(data.get(standardized_team, "0"))
                opponent_stats[opponent]["losses"] += int(data.get("Opponent", "0"))
                opponent_stats[opponent]["no_results"] += int(data.get("No Result", "0"))
                opponent_stats[opponent]["total"] += int(data.get("Total", "0"))
            
            if not opponent_stats:
                dispatcher.utter_message(text="Sorry, I didn't get that. Can you please rephrase your question")
                return []
            
            message = f"{standardized_team} performance against all opponents:\n\n"
            
            for opponent, stats in opponent_stats.items():
                if stats["total"] > 0:
                    win_percentage = (stats["wins"] / (stats["total"] - stats["no_results"])) * 100 if (stats["total"] - stats["no_results"]) > 0 else 0
                    message += f"vs {opponent}: {stats['wins']} wins, {stats['losses']} losses ({win_percentage:.1f}%)\n"
            
            dispatcher.utter_message(text=message)
        except Exception as e:
            dispatcher.utter_message(text="Sorry, I didn't get that. Can you please rephrase your question")
        
        return []


class action_team_no_result_matches(FirebaseAction):
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        team = tracker.get_slot("team")
        standardized_team = self.standardize_team_name(team)
        
        if not standardized_team:
            dispatcher.utter_message(text="Please specify a team to check their no-result matches.")
            return []
            
        collection = self.collection_name(standardized_team)
        query_ref = db.collection(collection)
        
        try:
            no_result_matches = []
            
            for doc in query_ref.stream():
                data = doc.to_dict()
                no_results = int(data.get("No Result", "0"))
                
                if no_results > 0:
                    no_result_matches.append({
                        "opponent": data.get("Against", ""),
                        "ground": data.get("Ground", ""),
                        "count": no_results
                    })
            
            if not no_result_matches:
                dispatcher.utter_message(text=f"{standardized_team} has no matches without a result.")
                return []
            
            total_no_results = sum(match["count"] for match in no_result_matches)
            
            message = f"{standardized_team} has {total_no_results} matches without a result:\n\n"
            for match in no_result_matches:
                message += f"{match['count']} vs {match['opponent']} at {match['ground']}\n"
            
            dispatcher.utter_message(text=message)
        except Exception as e:
            dispatcher.utter_message(text="Sorry, I didn't get that. Can you please rephrase your question")
        
        return []


class action_head_to_head_by_ground(FirebaseAction):
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        team = tracker.get_slot("team")
        opponent = tracker.get_slot("opponent")
        ground = tracker.get_slot("ground")
        
        standardized_team = self.standardize_team_name(team)
        standardized_opponent = self.standardize_team_name(opponent)
        standardized_ground = self.standardize_ground_name(ground)
        
        if not standardized_team or not standardized_opponent or not standardized_ground:
            dispatcher.utter_message(text="Please specify both teams and the ground to check their head-to-head record.")
            return []
            
        collection = self.collection_name(standardized_team)
        query_ref = db.collection(collection)
        
        try:
            results = []
            
            for doc in query_ref.stream():
                data = doc.to_dict()
                if (standardized_opponent.lower() in data.get("Against", "").lower() and 
                    standardized_ground.lower() in data.get("Ground", "").lower()):
                    results.append(data)
            
            if not results:
                dispatcher.utter_message(text=f"I couldn't find any matches between {standardized_team} and {standardized_opponent} at {standardized_ground}.")
                return []
                
            total_team_wins = 0
            total_opponent_wins = 0
            total_no_results = 0
            total_matches = 0
            
            for result in results:
                team_wins = int(result.get(standardized_team, "0"))
                opponent_wins = int(result.get("Opponent", "0"))
                no_results = int(result.get("No Result", "0"))
                
                total_team_wins += team_wins
                total_opponent_wins += opponent_wins
                total_no_results += no_results
                total_matches += int(result.get("Total", "0"))
                
            message = f"{standardized_team} vs {standardized_opponent} at {standardized_ground}:\n"
            message += f"{standardized_team} wins: {total_team_wins}\n"
            message += f"{standardized_opponent} wins: {total_opponent_wins}\n"
            message += f"No Results: {total_no_results}\n"
            message += f"Total Matches: {total_matches}"
            
            dispatcher.utter_message(text=message)
        except Exception as e:
            dispatcher.utter_message(text="Sorry, I didn't get that. Can you please rephrase your question")
        
        return []


class action_most_dominant_team_at_venue(FirebaseAction):
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ground = tracker.get_slot("ground")
        standardized_ground = self.standardize_ground_name(ground)
        
        if not standardized_ground:
            dispatcher.utter_message(text="Please specify a ground to check the most dominant team there.")
            return []
            
        # We need to check all team collections
        team_collections = [
            "CSK_with_All", "DC_with_All", "DCH_with_All", "GL_with_All", "GT_with_All", 
            "KKR_with_All", "KTK_with_All", "LSG_with_All", "MI_with_All", "PBKS_with_All", 
            "PWI_with_All", "RCB_With_All", "RPS_with_All", "RR_with_All", "SRH_with_All"
        ]
        
        try:
            team_stats = {}
            
            for collection_name in team_collections:
                query_ref = db.collection(collection_name)
                team_name = None
                
                # Extract team name from collection name
                for short_name, full_name in team_name_mapping.items():
                    if short_name.upper() in collection_name:
                        team_name = full_name
                        break
                
                if not team_name:
                    continue
                    
                # Find matches at the specified ground
                for doc in query_ref.stream():
                    data = doc.to_dict()
                    if standardized_ground.lower() in data.get("Ground", "").lower():
                        if team_name not in team_stats:
                            team_stats[team_name] = {
                                "wins": 0,
                                "total": 0
                            }
                        team_stats[team_name]["wins"] += int(data.get(team_name, "0"))
                        team_stats[team_name]["total"] += int(data.get("Total", "0"))
            
            if not team_stats:
                dispatcher.utter_message(text=f"I couldn't find any match data for {standardized_ground}.")
                return []
            
            # Calculate win percentages and find the most dominant team
            best_team = None
            best_win_percentage = 0
            
            for team, stats in team_stats.items():
                if stats["total"] > 0:
                    win_percentage = (stats["wins"] / stats["total"]) * 100
                    stats["win_percentage"] = win_percentage
                    
                    if win_percentage > best_win_percentage and stats["total"] >= 5:  # Minimum 5 matches to be considered
                        best_win_percentage = win_percentage
                        best_team = team
            
            if best_team:
                message = f"Most dominant team at {standardized_ground}:\n\n"
                message += f"{best_team} with a win percentage of {team_stats[best_team]['win_percentage']:.2f}%\n"
                message += f"({team_stats[best_team]['wins']} wins in {team_stats[best_team]['total']} matches)\n\n"
                
                # Show top 3 teams
                message += "Other teams at this venue:\n"
                sorted_teams = sorted(team_stats.items(), key=lambda x: x[1].get("win_percentage", 0), reverse=True)
                
                for i, (team, stats) in enumerate(sorted_teams[:3], 1):
                    if team != best_team and stats["total"] >= 5:
                        win_percentage = stats.get("win_percentage", 0)
                        message += f"{team}: {win_percentage:.2f}% ({stats['wins']}/{stats['total']})\n"
                
                dispatcher.utter_message(text=message)
            else:
                dispatcher.utter_message(text=f"No team has played enough matches at {standardized_ground} to determine dominance.")
        except Exception as e:
            dispatcher.utter_message(text="Sorry, I didn't get that. Can you please rephrase your question")
        
        return []

# ------------------------------------------------------------------------------------------------------------------------

# Group 9 - Team Performance
class action_all_ipl_match_data_yearwise(FirebaseAction):
    def collection_name(self) -> Text:
        return "All_ipl_match_data_yearwise_scorecard"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"Match {doc['MatchCode']} ({doc['Year']}): {doc['Teams']} at {doc['Venue']}. {doc['Win_By']}. {doc['Player_of_Match']} was Player of the Match."


class action_team_performance_yearwise(FirebaseAction):
    def collection_name(self) -> Text:
        return "All_Years_Teams_Performance"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Team']} ({doc['Abbreviation']}) in {doc['Season']}: Played {doc['Played']} matches, Won {doc['Won']}, Lost {doc['Lost']}."


class action_close_matches_by_wickets(FirebaseAction):
    def collection_name(self) -> Text:
        return "Close_Matches_by_Wickets"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"On {doc['Date']}, {doc['Team']} achieved {doc['Achieved_Score']} chasing {doc['Target_Runs']} against {doc['Opponent']} at {doc['Venue']}. {doc['Match_Result']}."


class action_end_moment_finish(FirebaseAction):
    def collection_name(self) -> Text:
        return "End_moment_finish"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"On {doc['Date']} at {doc['Ground']}, {doc['Winner']} defeated {doc['Opponent']} by just {doc['Margin']}."


class action_highest_match_total_scores(FirebaseAction):
    def collection_name(self) -> Text:
        return "Highest_Match_Total_Scores"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"Total of {doc['Total_Runs_(Both_Teams)']} runs scored in the match between {doc['Team']} and {doc['Opponent']} at {doc['Venue']} on {doc['Date']}. {doc['Result']}."


class action_highest_partnerships(FirebaseAction):
    def collection_name(self) -> Text:
        return "Highest_Partnerships"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Batsmen_Involved']} of {doc['Batting_Team']} put on {doc['Partnership_Runs']} runs for the {doc['Wicket_Position']} wicket against {doc['Opposing_Team']} at {doc['Stadium_Name']} on {doc['Match_Date']}."


class action_highest_run_chase(FirebaseAction):
    def collection_name(self) -> Text:
        return "Highest_Run_Chase"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Team']} chased down {doc['Target_Score']} making {doc['Runs_Scored']} against {doc['Opposing_Team']} at {doc['Stadium_Name']}. {doc['Match_Result']} on {doc['Match_Date']}."


class action_highest_scores_teamwise(FirebaseAction):
    def collection_name(self) -> Text:
        return "Highest_Scores_Teamwise_Overall"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Team']} scored {doc['Score']} against {doc['Versus']} at {doc['Venue']}. {doc['Result']} on {doc['Scorecard']}."


class action_highest_scores(FirebaseAction):
    def collection_name(self) -> Text:
        return "Highest_Scores"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Batting_Team']} scored {doc['Runs_Scored']} against {doc['Opposing_Team']} at {doc['Stadium_Name']}. {doc['Match_Result']} on {doc['Match_Date']}."


class action_highest_successful_run_chases(FirebaseAction):
    def collection_name(self) -> Text:
        return "Highest_Successful_Run_Chases"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Team']} successfully chased {doc['Target']} scoring {doc['Score']} against {doc['Opponent']} at {doc['Venue']}. {doc['Result']} on {doc['Date']}."


class action_ipl_points_table(FirebaseAction):
    def collection_name(self) -> Text:
        return "IPL_Points_Table_2008_2024"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Team']} in {doc['Season']}: Played {doc['Matches_Played']}, Won {doc['Matches_Won']}, Lost {doc['Matches_Lost']}, Points {doc['Total_Points']}, NRR {doc['Net_Run_Rate']}, Final Position: {doc['Final_Position']}."


class action_lowest_scores_ipl(FirebaseAction):
    def collection_name(self) -> Text:
        return "Lowest_Scores_IPL"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Team']} were bowled out for just {doc['Score']} against {doc['Versus']} at {doc['Venue']}. {doc['Result']} on {doc['Date']}."


class action_lowest_scores_teamwise(FirebaseAction):
    def collection_name(self) -> Text:
        return "Lowest_Scores_Teamwise"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Team']} were bowled out for just {doc['Score']} against {doc['Opponent']} at {doc['Venue']}. {doc['Result']} on {doc['Date']}."


class action_one_sided_finish(FirebaseAction):
    def collection_name(self) -> Text:
        return "One_sided_finish"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"On {doc['Date']} at {doc['Ground']}, {doc['Winner']} crushed {doc['Opponent']} by a huge margin of {doc['Margin']}."


class action_top_partnerships_by_team(FirebaseAction):
    def collection_name(self) -> Text:
        return "Top_10_Partnerships_by_Team"

    def format_response(self, doc: Dict[Text, Any]) -> Text:
        return f"{doc['Batsmen_Involved']} of {doc['Batting_Team']} put on {doc['Runs']} runs for the {doc['Wicket_Position']} wicket against {doc['Opposing_Team']} at {doc['Stadium_Name']} on {doc['Match_Date']}."


# Fallback action
class action_fallback(Action):
    def name(self) -> Text:
        return "action_fallback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Sorry, I didn't get that. Can you please rephrase your question")
        return []