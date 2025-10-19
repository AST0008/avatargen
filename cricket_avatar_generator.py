import requests
import json
import time
import os
from typing import Dict, List

class AvatarVideoGenerator:
    """
    Integrate with HeyGen or D-ID API to create AI avatar commentary videos
    """
    
    def __init__(self, provider="heygen", api_key=None):
        """
        Initialize avatar generator
        provider: 'heygen' or 'd-id'
        """
        self.provider = provider
        self.api_key = api_key
        self.output_dir = "avatar_videos"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # API endpoints
        self.endpoints = {
            "heygen": {
                "create": "https://api.heygen.com/v2/video/generate",
                "status": "https://api.heygen.com/v1/video_status.get"
            },
            "d-id": {
                "create": "https://api.d-id.com/talks",
                "status": "https://api.d-id.com/talks/{talk_id}"
            }
        }
        
        # Avatar configurations
        self.avatar_configs = {
            "heygen": {
                "avatar_id": "Thaddeus_Black_Suit_public",  # Sample avatar ID
                "voice_id": "2b5a8ab8a0a74166a031d6eda4321600"
            },
            "d-id": {
                "presenter_id": "amy-Aq6OmGZnMt",  # Sample presenter
                "voice_id": "en-US-JennyNeural"
            }
        }

    def test_voices(self):
        """Tests the API key by trying to list available voices."""
        test_url = "https://api.heygen.com/v2/voices"
        headers = {
            "x-api-key": self.api_key,
            "accept": "application/json"
        }
        print(f"\n🔬 Testing API key with GET request to: {test_url}")
        try:
            response = requests.get(test_url, headers=headers, timeout=10)
            print(f"Test Response Status: {response.status_code}")
            print("Test Response Body (first 1000 chars):")
            print(response.text[:1000] + "...") # Print only the start of the list
        except Exception as e:
            print(f"❌ Test request failed: {e}")
    
    def test_api_key(self):
        """Tests the API key by trying to list available avatars."""
        test_url = "https://api.heygen.com/v2/avatars"
        headers = {
            "x-api-key": self.api_key,
            "accept": "application/json"
        }
        print(f"🔬 Testing API key with GET request to: {test_url}")
        try:
            response = requests.get(test_url, headers=headers, timeout=10)
            print(f"Test Response Status: {response.status_code}")
            print("Test Response Body:")
            print(response.text)
            return response.status_code
        except Exception as e:
            print(f"❌ Test request failed: {e}")
            return None


    def create_avatar_video_heygen(self, script: str, segment_id: int) -> Dict:
        """Create video using HeyGen API"""
        
        if not self.api_key:
            print(f"⚠️  No API key provided. Creating mock response for segment {segment_id}")
            return self._create_mock_response(segment_id, script)
        
        headers = {
            "x-api-key": self.api_key,       # Use lowercase 'x-api-key'
            "Content-Type": "application/json",
            "accept": "application/json"  # Add this line
        }
        print("headers", headers)


        payload = {
            "video_inputs": [{
                # "character": {
                #     "type": "avatar",
                #     "avatar_id": self.avatar_configs["heygen"]["avatar_id"],
                #     "avatar_style": "normal"
                # },
                "character": {
                "type": "talking_photo",
                # "avatar_id": "Daisy-inskirt-20220818",
                "talking_photo_id":"7ae960f017754f06ac14ad8c9579c839"
                # "avatar_style": "normal"
                },
                "voice": {
                    "type": "text",
                    "input_text": script,
                    "voice_id": self.avatar_configs["heygen"]["voice_id"]
                },
                # "background": {
                #     "type": "color",
                #     "value": "#1C1C1C"
                # }
            }],
                "dimension": {
                 "width": 1280,   # <-- CHANGE THIS
                 "height": 720    # <-- CHANGE THIS
                },
            # "aspect_ratio": "16:9"
        }
        
        print("[ayload]", payload)

        try:
            response = requests.post(
                self.endpoints["heygen"]["create"],
                headers=headers,
                json=payload,
                timeout=30
            )
            print("response \n\n\n",response)
            response.raise_for_status()
            result = response.json()
            
            return {
                "provider": "heygen",
                "video_id": result.get("data", {}).get("video_id"),
                "status": "processing",
                "segment_id": segment_id
            }
        
        except Exception as e:
            print(f"❌ Error creating HeyGen video: {e}")
            return self._create_mock_response(segment_id, script)
    
    def create_avatar_video_did(self, script: str, segment_id: int) -> Dict:
        """Create video using D-ID API"""
        
        if not self.api_key:
            print(f"⚠️  No API key provided. Creating mock response for segment {segment_id}")
            return self._create_mock_response(segment_id, script)
        
        headers = {
            "Authorization": f"Basic {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "script": {
                "type": "text",
                "input": script,
                "provider": {
                    "type": "microsoft",
                    "voice_id": self.avatar_configs["d-id"]["voice_id"]
                }
            },
            "config": {
                "fluent": True,
                "pad_audio": 0
            },
            "source_url": f"https://create-images-results.d-id.com/DefaultPresenters/{self.avatar_configs['d-id']['presenter_id']}/image.png"
        }
        
        try:
            response = requests.post(
                self.endpoints["d-id"]["create"],
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            return {
                "provider": "d-id",
                "video_id": result.get("id"),
                "status": "processing",
                "segment_id": segment_id
            }
        
        except Exception as e:
            print(f"❌ Error creating D-ID video: {e}")
            return self._create_mock_response(segment_id, script)
    
    def _create_mock_response(self, segment_id: int, script: str) -> Dict:
        """Create mock response for testing without API"""
        return {
            "provider": "mock",
            "video_id": f"mock_video_{segment_id}_{int(time.time())}",
            "status": "completed",
            "segment_id": segment_id,
            "video_url": f"mock_avatar_segment_{segment_id}.mp4",
            "duration": len(script.split()) * 0.4  # Estimate ~0.4 sec per word
        }
    
    def check_video_status(self, video_id: str, provider: str = None) -> Dict:
        """Check the status of video generation"""
        
        provider = provider or self.provider
        
        if provider == "mock":
            return {
                "status": "completed",
                "video_url": f"mock_video_{video_id}.mp4"
            }
        
        if not self.api_key:
            return {"status": "completed", "video_url": f"mock_{video_id}.mp4"}
        
        if provider == "heygen":
            headers = {"x-Api-Key": self.api_key}
            response = requests.get(
                self.endpoints["heygen"]["status"],
                headers=headers,
                params={"video_id": video_id},
                timeout=30
            )
            
        elif provider == "d-id":
            headers = {"Authorization": f"Basic {self.api_key}"}
            url = self.endpoints["d-id"]["status"].format(talk_id=video_id)
            response = requests.get(url, headers=headers, timeout=30)
        
        try:
            response.raise_for_status()
            result = response.json()
            
            if provider == "heygen":
                return {
                    "status": result.get("data", {}).get("status"),
                    "video_url": result.get("data", {}).get("video_url")
                }
            elif provider == "d-id":
                return {
                    "status": result.get("status"),
                    "video_url": result.get("result_url")
                }
        
        except Exception as e:
            print(f"❌ Error checking status: {e}")
            return {"status": "error", "video_url": None}
    
    def download_video(self, video_url: str, filename: str) -> str:
        """Download the generated video"""
        
        if video_url.startswith("mock_"):
            # Create a mock video file
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, 'w') as f:
                f.write(f"Mock video placeholder: {video_url}")
            return filepath
        
        try:
            response = requests.get(video_url, stream=True, timeout=60)
            response.raise_for_status()
            
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return filepath
        
        except Exception as e:
            print(f"❌ Error downloading video: {e}")
            return None
    
    def generate_commentary_videos(self, segments: List[Dict]) -> List[Dict]:
            """
            Generate avatar videos for all commentary segments
            """
            
            video_tasks = []
            
            print(f"\n🎬 Generating avatar videos using {self.provider.upper()}...\n")
            
            # 1. Create all video tasks first
            for segment in segments:
                print(f"Creating video for Segment {segment['id']}: {segment['type']}")
                print(f"Script length: {len(segment['script'])} characters")
                
                if self.provider == "heygen":
                    task = self.create_avatar_video_heygen(
                        segment['script'], 
                        segment['id']
                    )
                elif self.provider == "d-id":
                    task = self.create_avatar_video_did(
                        segment['script'],
                        segment['id']
                    )
                else:
                    task = self._create_mock_response(segment['id'], segment['script'])
                
                video_tasks.append(task)
                print(f"✅ Video task created: {task['video_id']}\n")
                
                # Small delay to avoid rate limiting
                time.sleep(1)
            
            # 2. Wait for all videos to complete using parallel polling
            print("⏳ Waiting for videos to generate...\n")
            
            completed_videos = []
            pending_tasks = list(video_tasks)  # Create a copy of the list to manage
            
            max_attempts = 60  # Wait up to 15 minutes (180 * 5s = 900s)
            attempt = 0

            while pending_tasks and attempt < max_attempts:
                attempt += 1
                print(f"--- Polling attempt {attempt}/{max_attempts} ---")
                
                # We must iterate over a copy of the list (tasks_to_check)
                # because we will be removing items from the original (pending_tasks)
                tasks_to_check = list(pending_tasks)
                
                for task in tasks_to_check:
                    
                    # Handle mock provider
                    if task['provider'] == 'mock':
                        print(f"✅ Segment {task['segment_id']} completed (mock)")
                        filepath = os.path.join(self.output_dir, f"segment_{task['segment_id']}.mp4")
                        with open(filepath, 'w') as f:
                            f.write(f"Mock video for segment {task['segment_id']}")
                        
                        completed_videos.append({
                            "segment_id": task['segment_id'],
                            "video_id": task['video_id'],
                            "status": "completed",
                            "local_path": filepath
                        })
                        pending_tasks.remove(task) # This task is done
                        continue # Go to the next task
                    
                    # Handle real API
                    status_info = self.check_video_status(
                        task['video_id'],
                        task['provider']
                    )
                    
                    if status_info['status'] == 'completed' and status_info['video_url']:
                        print(f"✅ Segment {task['segment_id']} completed!")
                        
                        # Download video
                        filename = f"segment_{task['segment_id']}.mp4"
                        local_path = self.download_video(
                            status_info['video_url'],
                            filename
                        )
                        
                        if local_path:
                            completed_videos.append({
                                "segment_id": task['segment_id'],
                                "video_id": task['video_id'],
                                "status": "completed",
                                "local_path": local_path
                            })
                        else:
                            print(f"❌ Segment {task['segment_id']} completed but download failed.")
                        
                        pending_tasks.remove(task) # This task is done
                    
                    elif status_info['status'] == 'error':
                        print(f"❌ Segment {task['segment_id']} failed to generate.")
                        pending_tasks.remove(task) # This task is also done (it failed)
                    
                    elif status_info['status'] == 'processing' or status_info['status'] == 'pending':
                        print(f"⏳ Segment {task['segment_id']}: Still {status_info['status']}...")
                    
                    else:
                        # Handle any other unexpected status
                        print(f"⚠️ Segment {task['segment_id']}: Unknown status '{status_info['status']}'")

                # Don't sleep if all tasks are done
                if pending_tasks:
                    time.sleep(5)  # Wait 5 seconds before polling ALL tasks again

            # After the loop, check if any tasks timed out
            if pending_tasks:
                print(f"\n❌ Timed out waiting for {len(pending_tasks)} video(s):")
                for task in pending_tasks:
                    print(f"  - Segment {task['segment_id']} (Video ID: {task['video_id']})")
            
            return completed_videos


# Usage Example
if __name__ == "__main__":
    # Load commentary script
    with open('commentary_script.json', 'r') as f:
        data = json.load(f)
    
    segments = data['segments']

    print("segments \n\n", segments)
    
    print("=" * 60)
    print("AI AVATAR VIDEO GENERATOR")
    print("=" * 60)
    
    # Initialize generator (mock mode - no API key needed)
    # avatar_generator = AvatarVideoGenerator(provider="heygen")
    
    # To use real APIs, uncomment and add your key:
    avatar_generator = AvatarVideoGenerator(
        provider="heygen",  # or "d-id"
        api_key="sk_V2_hgu_k2oGOq8IZ5C_qAM4vec0OtyoIEH7dte6utE5ZFhonF06"
    )


    # # --- ADD THIS TEST ---
    # print("\n🔬 CONDUCTING Voice TEST...")
    # avatar_generator.test_voices()
    # print("=" * 60)
    # # ---------------------
    
    # Generate videos
    completed_videos = avatar_generator.generate_commentary_videos(segments)
    print("completed videos \n\n", completed_videos)
    
    print("\n" + "=" * 60)
    print(f"✅ Generated {len(completed_videos)} avatar videos!")
    print("=" * 60)
    
    for video in completed_videos:
        print(f"  Segment {video['segment_id']}: {video['local_path']}")
    
    # Save video info for final composition
    with open('avatar_videos.json', 'w') as f:
        json.dump(completed_videos, f, indent=2)
    
    print("\n💡 API Integration Notes:")
    print("   HeyGen: https://docs.heygen.com/")
    print("   D-ID: https://docs.d-id.com/")
    print("   Both require paid API keys for production use")


