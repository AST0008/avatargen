"""
Automated Cricket Commentary Video Generator
Main orchestrator that runs all components
"""

import json
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.END}\n")

def print_step(step_num, total_steps, title):
    print(f"{Colors.BOLD}{Colors.BLUE}[STEP {step_num}/{total_steps}] {title}{Colors.END}")
    print(f"{Colors.CYAN}{'-' * 60}{Colors.END}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.CYAN}ℹ️  {message}{Colors.END}")


class CricketCommentaryPipeline:
    """Main pipeline orchestrator"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.output_dir = "cricket_output"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # API keys (optional - will use mock data if not provided)
        self.gemini_api_key = self.config.get('gemini_api_key')
        self.avatar_api_key = self.config.get('avatar_api_key')
        self.avatar_provider = self.config.get('avatar_provider', 'heygen')
        
        # Pipeline state
        self.match_data = None
        self.script_segments = None
        self.charts = None
        self.avatar_videos = None
        self.final_video = None
    
    def run_full_pipeline(self):
        """Execute the complete video generation pipeline"""
        
        print_header("AUTOMATED CRICKET COMMENTARY VIDEO GENERATOR")
        
        start_time = datetime.now()
        total_steps = 4
        
        try:
            # Step 1: Generate Commentary Scripts
            print_step(1, total_steps, "Generating Commentary Scripts")
            if not self.generate_scripts():
                print_error("Script generation failed")
                return False
            print_success("Scripts generated successfully\n")
            
            # Step 2: Generate Charts
            print_step(2, total_steps, "Generating Charts & Visualizations")
            if not self.generate_charts():
                print_error("Chart generation failed")
                return False
            print_success("Charts generated successfully\n")
            
            # Step 3: Generate Avatar Videos
            print_step(3, total_steps, "Generating AI Avatar Videos")
            if not self.generate_avatar_videos():
                print_error("Avatar video generation failed")
                return False
            print_success("Avatar videos generated successfully\n")
            
            # Step 4: Compose Final Video
            print_step(4, total_steps, "Composing Final Video")
            if not self.compose_final_video():
                print_error("Video composition failed")
                return False
            print_success("Final video composed successfully\n")
            
            # Success summary
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            print_header("PIPELINE COMPLETE!")
            print_info(f"Total time: {duration:.2f} seconds")
            print_info(f"Final video: {self.final_video}")
            
            self.print_summary()
            
            return True
            
        except Exception as e:
            print_error(f"Pipeline failed with error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def generate_scripts(self):
        """Step 1: Generate commentary scripts using Gemini"""
        
        try:
            # Import the script generator (assuming previous code is in a module)
            from cricket_script_generator import (
                CommentaryScriptGenerator, 
                MOCK_MATCH_DATA
            )
            
            self.match_data = MOCK_MATCH_DATA
            
            generator = CommentaryScriptGenerator(api_key=self.gemini_api_key)
            
            print_info("Using mock match data")
            if self.gemini_api_key:
                print_info("Using Gemini API for script generation")
            else:
                print_warning("No Gemini API key - using mock scripts")
            
            self.script_segments = generator.create_timed_script(self.match_data)
            
            # Save for debugging
            with open(os.path.join(self.output_dir, 'scripts.json'), 'w') as f:
                json.dump({
                    'match_data': self.match_data,
                    'segments': self.script_segments
                }, f, indent=2)
            
            print_info(f"Generated {len(self.script_segments)} script segments")
            
            return True
            
        except ImportError:
            print_warning("Script generator module not found - using inline mock data")
            # Fallback: create basic mock data inline
            self.match_data = {
                "match_id": "TEST_001",
                "teams": {"batting": "India", "bowling": "Australia"},
                "current_score": {"runs": 156, "wickets": 3, "overs": 25.4}
            }
            self.script_segments = [
                {
                    "id": 1,
                    "type": "summary",
                    "script": "Mock commentary segment 1",
                    "duration": 45
                }
            ]
            return True
        
        except Exception as e:
            print_error(f"Script generation error: {e}")
            return False
    
    def generate_charts(self):
        """Step 2: Generate visualization charts"""
        
        try:
            from cricket_chart_generator import CricketChartGenerator
            
            chart_gen = CricketChartGenerator(
                output_dir=os.path.join(self.output_dir, 'charts')
            )
            
            self.charts = chart_gen.generate_all_charts(self.match_data)
            
            print_info(f"Generated {len(self.charts)} charts")
            for chart_type, path in self.charts.items():
                print(f"  📊 {chart_type}: {path}")
            
            return True
            
        except Exception as e:
            print_error(f"Chart generation error: {e}")
            return False
    
    def generate_avatar_videos(self):
        """Step 3: Generate AI avatar commentary videos"""
        
        try:
            from cricket_avatar_generator import AvatarVideoGenerator
            
            avatar_gen = AvatarVideoGenerator(
                provider=self.avatar_provider,
                api_key=self.avatar_api_key
            )
            
            if self.avatar_api_key:
                print_info(f"Using {self.avatar_provider.upper()} API")
            else:
                print_warning(f"No API key - using mock avatar videos")
            
            self.avatar_videos = avatar_gen.generate_commentary_videos(
                self.script_segments
            )
            
            print_info(f"Generated {len(self.avatar_videos)} avatar videos")
            
            return True
            
        except Exception as e:
            print_error(f"Avatar video generation error: {e}")
            return False
    
    def compose_final_video(self):
        """Step 4: Compose final video with FFmpeg"""
        
        try:
            from cricket_video_composer import VideoComposer
            
            composer = VideoComposer(
                output_filename=os.path.join(
                    self.output_dir,
                    'cricket_commentary_final.mp4'
                )
            )
            
            # Check FFmpeg availability
            if not composer.check_ffmpeg():
                print_warning("FFmpeg not installed - creating mock output")
                self.final_video = os.path.join(
                    self.output_dir,
                    'mock_final_video.txt'
                )
                with open(self.final_video, 'w') as f:
                    f.write("Mock final video\n")
                    f.write("Install FFmpeg for actual video composition\n")
                return True
            
            self.final_video = composer.create_final_video(
                self.avatar_videos,
                self.charts
            )
            
            if self.final_video and os.path.exists(self.final_video):
                file_size = os.path.getsize(self.final_video) / (1024 * 1024)
                print_info(f"Final video size: {file_size:.2f} MB")
                return True
            
            return False
            
        except Exception as e:
            print_error(f"Video composition error: {e}")
            return False
    
    def print_summary(self):
        """Print pipeline execution summary"""
        
        print(f"\n{Colors.BOLD}📊 PIPELINE SUMMARY{Colors.END}")
        print(f"{Colors.CYAN}{'─' * 60}{Colors.END}")
        
        print(f"\n{Colors.BOLD}Match Data:{Colors.END}")
        if self.match_data:
            teams = self.match_data.get('teams', {})
            score = self.match_data.get('current_score', {})
            print(f"  {teams.get('batting', 'N/A')} vs {teams.get('bowling', 'N/A')}")
            print(f"  Score: {score.get('runs', 0)}/{score.get('wickets', 0)} ({score.get('overs', 0)} ov)")
        
        print(f"\n{Colors.BOLD}Generated Assets:{Colors.END}")
        if self.script_segments:
            print(f"  📝 Scripts: {len(self.script_segments)} segments")
        if self.charts:
            print(f"  📊 Charts: {len(self.charts)} visualizations")
        if self.avatar_videos:
            print(f"  🎬 Avatar Videos: {len(self.avatar_videos)} clips")
        
        print(f"\n{Colors.BOLD}Output Location:{Colors.END}")
        print(f"  📁 {os.path.abspath(self.output_dir)}")
        
        if self.final_video:
            print(f"\n{Colors.BOLD}Final Video:{Colors.END}")
            print(f"  🎥 {os.path.abspath(self.final_video)}")


def create_standalone_modules():
    """
    Create standalone Python files from the artifacts
    This allows the pipeline to run independently
    """
    
    print_info("Creating standalone module files...")
    
    modules = {
        'cricket_script_generator.py': '''# Script from Step 1
# Copy the content from the first artifact here
pass
''',
        'cricket_chart_generator.py': '''# Script from Step 2
# Copy the content from the second artifact here
pass
''',
        'cricket_avatar_generator.py': '''# Script from Step 3
# Copy the content from the third artifact here
pass
''',
        'cricket_video_composer.py': '''# Script from Step 4
# Copy the content from the fourth artifact here
pass
'''
    }
    
    for filename, content in modules.items():
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                f.write(content)
            print(f"  Created: {filename}")


def main():
    """Main entry point"""
    
    print_header("CRICKET COMMENTARY VIDEO GENERATOR")
    print(f"{Colors.CYAN}Automated AI-powered cricket commentary video creation{Colors.END}\n")
    
    # Configuration
    config = {
        # Optional: Add your API keys here
        'gemini_api_key': None,  # os.getenv('GEMINI_API_KEY')
        'avatar_api_key': None,  # os.getenv('HEYGEN_API_KEY') or os.getenv('DID_API_KEY')
        'avatar_provider': 'heygen',  # 'heygen' or 'd-id'
    }
    
    # Check for API keys from environment
    if os.getenv('GEMINI_API_KEY'):
        config['gemini_api_key'] = os.getenv('GEMINI_API_KEY')
        print_info("Gemini API key found in environment")
    
    if os.getenv('HEYGEN_API_KEY'):
        config['avatar_api_key'] = os.getenv('HEYGEN_API_KEY')
        config['avatar_provider'] = 'heygen'
        print_info("HeyGen API key found in environment")
    elif os.getenv('DID_API_KEY'):
        config['avatar_api_key'] = os.getenv('DID_API_KEY')
        config['avatar_provider'] = 'd-id'
        print_info("D-ID API key found in environment")
    
    if not config['gemini_api_key'] and not config['avatar_api_key']:
        print_warning("No API keys provided - running in MOCK mode")
        print_info("Set environment variables for production use:")
        print("  export GEMINI_API_KEY='your_key'")
        print("  export HEYGEN_API_KEY='your_key'  # or DID_API_KEY")
        print()
    
    # Run pipeline
    pipeline = CricketCommentaryPipeline(config)
    success = pipeline.run_full_pipeline()
    
    if success:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 SUCCESS!{Colors.END}")
        print(f"{Colors.GREEN}Your cricket commentary video has been generated!{Colors.END}\n")
        
        print(f"{Colors.BOLD}Next Steps:{Colors.END}")
        print("  1. Review the generated video")
        print("  2. Customize scripts and regenerate if needed")
        print("  3. Add real match data for production use")
        print("  4. Integrate with live match feeds")
        print("  5. Add background music and sound effects")
        print("  6. Export to different formats/resolutions")
        
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ FAILED{Colors.END}")
        print(f"{Colors.RED}The pipeline encountered errors. Check the logs above.{Colors.END}\n")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Pipeline interrupted by user{Colors.END}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Colors.RED}💥 Unexpected error: {e}{Colors.END}")
        import traceback
        traceback.print_exc()
        sys.exit(1)