import subprocess
import json
import os
from typing import List, Dict

class VideoComposer:
    """
    Compose final cricket commentary video using FFmpeg
    Combines avatar videos, charts, transitions, and audio
    """
    
    def __init__(self, output_filename="cricket_commentary_final.mp4"):
        self.output_filename = output_filename
        self.temp_dir = "temp_video_files"
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Video settings
        self.resolution = "1920x1080"
        self.fps = 30
        self.audio_codec = "aac"
        self.video_codec = "libx264"
    
    def check_ffmpeg(self) -> bool:
        """Check if FFmpeg is installed"""
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def create_image_video(self, image_path: str, duration: float, output_path: str) -> bool:
        """Convert static image to video with specified duration"""
        
        command = [
            'ffmpeg',
            '-loop', '1',
            '-i', image_path,
            '-c:v', self.video_codec,
            '-t', str(duration),
            '-pix_fmt', 'yuv420p',
            '-vf', f'scale={self.resolution}',
            '-r', str(self.fps),
            '-y',  # Overwrite output
            output_path
        ]
        
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.returncode == 0
        except Exception as e:
            print(f"❌ Error creating image video: {e}")
            return False
    
    def add_fade_transition(self, input_path: str, output_path: str, 
                           fade_in: float = 0.5, fade_out: float = 0.5) -> bool:
        """Add fade in/out transitions to a video"""
        
        # Get video duration first
        probe_cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            input_path
        ]
        
        try:
            result = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=10)
            duration = float(result.stdout.strip())
            
            fade_out_start = duration - fade_out
            
            command = [
                'ffmpeg',
                '-i', input_path,
                '-vf', f'fade=t=in:st=0:d={fade_in},fade=t=out:st={fade_out_start}:d={fade_out}',
                '-c:a', 'copy',
                '-y',
                output_path
            ]
            
            result = subprocess.run(command, capture_output=True, text=True, timeout=60)
            return result.returncode == 0
        
        except Exception as e:
            print(f"❌ Error adding transitions: {e}")
            return False
    
    def add_lower_third(self, input_path: str, output_path: str, 
                       text: str, position: str = "bottom") -> bool:
        """Add text overlay (lower third) to video"""
        
        # Position settings
        if position == "bottom":
            y_pos = "main_h-100"
        elif position == "top":
            y_pos = "50"
        else:
            y_pos = "main_h/2"
        
        command = [
            'ffmpeg',
            '-i', input_path,
            '-vf', (
                f"drawtext=text='{text}':"
                f"fontsize=36:fontcolor=white:box=1:boxcolor=black@0.7:"
                f"boxborderw=10:x=(w-text_w)/2:y={y_pos}"
            ),
            '-c:a', 'copy',
            '-y',
            output_path
        ]
        
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=60)
            return result.returncode == 0
        except Exception as e:
            print(f"❌ Error adding lower third: {e}")
            return False
    
    def create_picture_in_picture(self, main_video: str, overlay_video: str,
                                  output_path: str, position: str = "topright") -> bool:
        """Create picture-in-picture effect (avatar + charts)"""
        
        # Position settings for overlay
        positions = {
            "topright": "main_w-overlay_w-20:20",
            "topleft": "20:20",
            "bottomright": "main_w-overlay_w-20:main_h-overlay_h-20",
            "bottomleft": "20:main_h-overlay_h-20"
        }
        
        overlay_pos = positions.get(position, positions["topright"])
        
        command = [
            'ffmpeg',
            '-i', main_video,
            '-i', overlay_video,
            '-filter_complex',
            f"[1:v]scale=640:360[overlay];[0:v][overlay]overlay={overlay_pos}",
            '-c:a', 'copy',
            '-y',
            output_path
        ]
        
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=120)
            return result.returncode == 0
        except Exception as e:
            print(f"❌ Error creating PIP: {e}")
            return False
    
    def concatenate_videos(self, video_list: List[str], output_path: str) -> bool:
        """Concatenate multiple videos into one"""
        
        # Create concat file
        concat_file = os.path.join(self.temp_dir, 'concat_list.txt')
        with open(concat_file, 'w') as f:
            for video_path in video_list:
                # Convert to absolute path
                abs_path = os.path.abspath(video_path)
                f.write(f"file '{abs_path}'\n")
        
        command = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_file,
            '-c', 'copy',
            '-y',
            output_path
        ]
        
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=180)
            return result.returncode == 0
        except Exception as e:
            print(f"❌ Error concatenating videos: {e}")
            return False
    
    def add_background_music(self, video_path: str, audio_path: str,
                            output_path: str, audio_volume: float = 0.2) -> bool:
        """Add background music to video"""
        
        command = [
            'ffmpeg',
            '-i', video_path,
            '-i', audio_path,
            '-filter_complex',
            f'[1:a]volume={audio_volume}[a1];[0:a][a1]amix=inputs=2:duration=first[aout]',
            '-map', '0:v',
            '-map', '[aout]',
            '-c:v', 'copy',
            '-c:a', self.audio_codec,
            '-y',
            output_path
        ]
        
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=180)
            return result.returncode == 0
        except Exception as e:
            print(f"❌ Error adding background music: {e}")
            return False
    
    def compose_segment(self, segment_info: Dict, chart_path: str = None) -> str:
        """Compose a single segment with avatar and optional chart"""
        
        segment_id = segment_info['segment_id']
        avatar_video = segment_info['local_path']
        
        output_path = os.path.join(
            self.temp_dir,
            f'composed_segment_{segment_id}.mp4'
        )
        
        print(f"  🎬 Composing segment {segment_id}...")
        
        # If no chart, just add transitions to avatar video
        if not chart_path:
            transition_path = os.path.join(
                self.temp_dir,
                f'transition_segment_{segment_id}.mp4'
            )
            if self.add_fade_transition(avatar_video, output_path, 0.5, 0.5):
                print(f"  ✅ Segment {segment_id} composed (avatar only)")
                return output_path
            return None
        
        # Convert chart to video
        chart_video = os.path.join(
            self.temp_dir,
            f'chart_video_{segment_id}.mp4'
        )
        
        if not self.create_image_video(chart_path, 8.0, chart_video):
            print(f"  ⚠️  Chart conversion failed, using avatar only")
            return avatar_video
        
        # Create picture-in-picture
        pip_path = os.path.join(
            self.temp_dir,
            f'pip_segment_{segment_id}.mp4'
        )
        
        if self.create_picture_in_picture(
            avatar_video, chart_video, pip_path, "bottomright"
        ):
            # Add transitions
            if self.add_fade_transition(pip_path, output_path, 0.5, 0.5):
                print(f"  ✅ Segment {segment_id} composed (with chart)")
                return output_path
        
        return avatar_video
    
    def create_final_video(self, segments: List[Dict], charts: Dict) -> str:
        """Create the final composed video"""
        
        print("\n" + "=" * 60)
        print("🎬 COMPOSING FINAL VIDEO")
        print("=" * 60 + "\n")
        
        # Check FFmpeg
        if not self.check_ffmpeg():
            print("❌ FFmpeg not found! Please install FFmpeg:")
            print("   Ubuntu/Debian: sudo apt-get install ffmpeg")
            print("   macOS: brew install ffmpeg")
            print("   Windows: Download from ffmpeg.org")
            print("\n📝 Creating mock final video instead...")
            
            mock_output = "mock_" + self.output_filename
            with open(mock_output, 'w') as f:
                f.write("Mock final video - FFmpeg required for actual composition\n")
                for seg in segments:
                    f.write(f"Segment {seg['segment_id']}: {seg['local_path']}\n")
            return mock_output
        
        print("✅ FFmpeg found!\n")
        
        # Map segments to charts
        chart_mapping = {
            1: charts.get('run_rate'),      # Summary with run rate
            2: None,                         # Key moment - avatar only
            3: charts.get('manhattan')       # Statistics with Manhattan
        }
        
        composed_segments = []
        
        # Compose each segment
        for segment in segments:
            chart_path = chart_mapping.get(segment['segment_id'])
            composed_path = self.compose_segment(segment, chart_path)
            
            if composed_path:
                composed_segments.append(composed_path)
        
        if not composed_segments:
            print("❌ No segments could be composed")
            return None
        
        # Concatenate all segments
        print(f"\n🔗 Concatenating {len(composed_segments)} segments...")
        
        if self.concatenate_videos(composed_segments, self.output_filename):
            print(f"\n✅ Final video created: {self.output_filename}")
            
            # Get file size
            file_size = os.path.getsize(self.output_filename) / (1024 * 1024)
            print(f"📦 File size: {file_size:.2f} MB")
            
            return self.output_filename
        else:
            print("❌ Failed to concatenate segments")
            return None


# Usage Example
if __name__ == "__main__":
    print("=" * 60)
    print("CRICKET COMMENTARY VIDEO COMPOSER")
    print("=" * 60)
    
    # Load data from previous steps
    try:
        with open('avatar_videos.json', 'r') as f:
            segments = json.load(f)
        
        with open('chart_paths.json', 'r') as f:
            charts = json.load(f)
    except FileNotFoundError:
        print("❌ Required input files not found!")
        print("   Please run the previous scripts first:")
        print("   1. Data & Script Generation")
        print("   2. Chart Generation")
        print("   3. Avatar Video Generation")
        exit(1)
    
    # Create composer
    composer = VideoComposer(output_filename="cricket_commentary_final.mp4")
    
    # Compose final video
    final_video = composer.create_final_video(segments, charts)
    
    if final_video:
        print("\n" + "=" * 60)
        print("🎉 VIDEO COMPOSITION COMPLETE!")
        print("=" * 60)
        print(f"\n📹 Final video: {final_video}")
        print("\n💡 Next steps:")
        print("   - Review the video")
        print("   - Add background music if desired")
        print("   - Export to different formats/resolutions")
        print("   - Upload to your platform")
    else:
        print("\n❌ Video composition failed")
        print("Check the error messages above for details")