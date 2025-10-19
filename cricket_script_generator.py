import json
from datetime import datetime
import google.generativeai as genai

# Mock Cricket Match Data
MOCK_MATCH_DATA = {
    "match_id": "RCB_vs_KKR_IPL2024_032",
    "teams": {
        "batting": "Royal Challengers Bengaluru",
        "bowling": "Kolkata Knight Riders"
    },
    "current_score": {
        "runs": 176,
        "wickets": 4,
        "overs": 17.1
    },
    "recent_overs": [
        {"over": 15, "runs": 14, "wickets": 0, "balls": [1, 6, 1, 1, 0, 5]},
        {"over": 16, "runs": 9, "wickets": 0, "balls": [1, 1, 4, 1, 0, 2]},
        {"over": 17, "runs": 12, "wickets": 1, "balls": [6, "W", 1, 1, 2, 2]}
    ],
    "key_moments": [
        {
            "type": "six",
            "over": 15.2,
            "description": "Glenn Maxwell hammers Sunil Narine over midwicket for SIX",
            "batsman": "Glenn Maxwell",
            "runs": 6
        },
        {
            "type": "boundary",
            "over": 16.3,
            "description": "Virat Kohli times it perfectly through covers for FOUR",
            "batsman": "Virat Kohli",
            "runs": 4
        },
        {
            "type": "wicket",
            "over": 17.2,
            "description": "Maxwell caught at long-on off Andre Russell",
            "batsman": "Glenn Maxwell",
            "bowler": "Andre Russell"
        }
    ],
    "partnerships": [
        {"batsmen": ["Virat Kohli", "Glenn Maxwell"], "runs": 72, "balls": 46}
    ],
    "run_rate": {
        "current": 10.26,
        "required": 9.2
    }
}


class CommentaryScriptGenerator:
    def __init__(self, api_key=None):
        """
        Initialize Gemini API
        For now, we'll create a mock version that doesn't require API key
        """
        self.api_key = api_key
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            self.model = None
    
    def generate_commentary_script(self, match_data, segment_type="summary"):
        """
        Generate commentary script based on match data
        segment_type: 'summary', 'key_moment', 'statistics'
        """
        
        if self.model:
            # Real Gemini API call
            prompt = self._create_prompt(match_data, segment_type)
            response = self.model.generate_content(prompt)
            print("response from gemini   \n\n", response.text)
            return response.text
        else:
            # Mock commentary for testing without API
            return self._generate_mock_commentary(match_data, segment_type)
    
    def _create_prompt(self, match_data, segment_type):
        """Create prompt for Gemini API"""
        
        base_prompt = f"""You are an expert cricket commentator. Generate exciting, 
        professional cricket commentary based on the following match situation:
        
        Match: {match_data['teams']['batting']} vs {match_data['teams']['bowling']}
        Score: {match_data['current_score']['runs']}/{match_data['current_score']['wickets']} 
        in {match_data['current_score']['overs']} overs
        Current Run Rate: {match_data['run_rate']['current']}
        Required Run Rate: {match_data['run_rate']['required']}
        """
        
        if segment_type == "summary":
            prompt = base_prompt + f"""
            
            Generate a 15-20 second engaging summary of the current match situation.
            Include the score, recent performance, and what's at stake.
            Make it exciting and natural, as if you're speaking to viewers.
            """
        
        elif segment_type == "key_moment":
            moment = match_data['key_moments'][-1]
            prompt = base_prompt + f"""
            
            Generate exciting 15-20 second commentary for this key moment:
            {moment['description']}
            
            Make it dramatic and capture the excitement of the moment!
            """
        
        elif segment_type == "statistics":
            prompt = base_prompt + f"""
            
            Generate a 15-20 second statistical analysis focusing on:
            - Current partnership: {match_data['partnerships'][-1]['runs']} runs
            - Recent over performance
            - Run rate comparison
            
            Keep it informative but engaging.
            """
        
        return prompt
    
    def _generate_mock_commentary(self, match_data, segment_type):
        """Generate mock commentary without API"""
        
        score = match_data['current_score']
        teams = match_data['teams']
        
        mock_scripts = {
            "summary": f"""What a thrilling contest we're witnessing here! 
            {teams['batting']} have posted {score['runs']} for {score['wickets']} 
            in {score['overs']} overs. The run rate is ticking along nicely at 
            {match_data['run_rate']['current']}, and with the required rate at 
            {match_data['run_rate']['required']}, this match is beautifully poised. 
            The crowd is on their feet as we head into the crucial middle overs!""",
            
            "key_moment": f"""And that's MASSIVE! What a shot! 
            {match_data['key_moments'][-1].get('batsman', 'The batsman')} 
            has absolutely smashed that one! {match_data['key_moments'][-1]['description']}. 
            The crowd erupts! This is why we love this game!""",
            
            "statistics": f"""Let's look at the numbers. The current partnership 
            between {match_data['partnerships'][-1]['batsmen'][0]} and 
            {match_data['partnerships'][-1]['batsmen'][1]} has already added 
            {match_data['partnerships'][-1]['runs']} runs. They're scoring at 
            over 7 runs per over, putting pressure back on the bowling side. 
            In the last three overs, we've seen {sum(o['runs'] for o in match_data['recent_overs'])} 
            runs scored. The momentum is shifting!"""
        }
        
        return mock_scripts.get(segment_type, mock_scripts["summary"])
    
    def create_timed_script(self, match_data):
        """Create a full script with timestamps for video segments"""
        
        segments = []
        
        # Introduction segment (0-45 seconds)
        segments.append({
            "id": 1,
            "type": "summary",
            "timestamp": "00:00:00",
            "duration": 20,
            "script": self.generate_commentary_script(match_data, "summary"),
            "visual": "scoreboard"
        })
        
        # Key moment segment (45-65 seconds)
        segments.append({
            "id": 2,
            "type": "key_moment",
            "timestamp": "00:00:20",
            "duration": 20,
            "script": self.generate_commentary_script(match_data, "key_moment"),
            "visual": "highlight_replay"
        })
        
        # Statistics segment (65-95 seconds)
        segments.append({
            "id": 3,
            "type": "statistics",
            "timestamp": "00:00:40",
            "duration": 20,
            "script": self.generate_commentary_script(match_data, "statistics"),
            "visual": "charts"
        })
        
        return segments


# Usage Example
if __name__ == "__main__":
    # Initialize without API key for mock data
    generator = CommentaryScriptGenerator(api_key="AIzaSyBEJ1YI2LM-FpEMQZAy-wk4U3_cdcbCzVI")
    
    print("=" * 60)
    print("CRICKET COMMENTARY SCRIPT GENERATOR")
    print("=" * 60)
    
    # Generate timed script
    script_segments = generator.create_timed_script(MOCK_MATCH_DATA)
    
    print("\n📋 Generated Commentary Script:\n")
    for segment in script_segments:
        print(f"Segment {segment['id']}: {segment['type'].upper()}")
        print(f"⏱️  Timestamp: {segment['timestamp']} | Duration: {segment['duration']}s")
        print(f"🎬 Visual: {segment['visual']}")
        print(f"📝 Script:\n{segment['script']}\n")
        print("-" * 60)
    
    # Save to JSON for next steps
    with open('commentary_script.json', 'w') as f:
        json.dump({
            "match_data": MOCK_MATCH_DATA,
            "segments": script_segments
        }, f, indent=2)
    
    print("\n✅ Script saved to 'commentary_script.json'")
    print("\n💡 To use real Gemini API:")
    print("   generator = CommentaryScriptGenerator(api_key='YOUR_API_KEY')")


    