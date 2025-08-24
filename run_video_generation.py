import os
import shutil
import re
from narakeet_official_example.narakeet_api import VideoAPI
import sys
sys.path.append('narakeet-official-example')
from narakeet_api import VideoAPI

def process_lesson(api, lesson_content, output_filepath):
    """
    Creates a temporary project for a single lesson, zips it,
    and sends it to Narakeet to build a video.
    """
    temp_dir = "temp_lesson_project"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Add Narakeet directives for voice and visuals
    directives = "(voice: ashley)\\n(visuals: suggest)\\n\\n"
    script_content = directives + lesson_content
    
    script_path = os.path.join(temp_dir, "script.md")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script_content)

    try:
        # Zip the temporary directory
        zip_file = api.zip_directory_into_tempfile(temp_dir)
        
        # Upload the zip
        upload_token = api.request_upload_token()
        api.upload_zip_file(upload_token, zip_file)
        
        # Start the build
        task = api.request_build_task(upload_token, "script.md")
        task_result = api.poll_until_finished(task['statusUrl'], print)
        
        # Download the result
        if task_result['succeeded']:
            temp_video_file = api.download_to_temp_file(task_result['result'])
            shutil.move(temp_video_file, output_filepath)
            print(f"SUCCESS: Video saved to {output_filepath}")
        else:
            raise Exception(task_result['message'])
            
    finally:
        # Clean up
        shutil.rmtree(temp_dir)
        if 'zip_file' in locals() and os.path.exists(zip_file):
            os.remove(zip_file)


def main():
    api_key = os.getenv("NARAKEET_API_KEY")
    if not api_key:
        print("FATAL ERROR: The NARAKEET_API_KEY environment variable is not set.")
        return

    api = VideoAPI(api_key)
    output_dir = "final_video_lessons"
    os.makedirs(output_dir, exist_ok=True)
    
    module_files = sorted([f for f in os.listdir('.') if f.startswith('Module_') and f.endswith('.md')])

    for module_file in module_files:
        print(f"\\n--- Processing Module: {module_file} ---")
        with open(module_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lessons = content.split('---')
        
        for i, lesson_content in enumerate(lessons):
            lesson_content = lesson_content.strip()
            if not lesson_content:
                continue
            
            lesson_num = i + 1
            module_base_name = os.path.splitext(module_file)[0]
            output_filepath = os.path.join(output_dir, f"{module_base_name}_Lesson_{lesson_num}.mp4")
            
            print(f"  > Starting Lesson {lesson_num}")
            try:
                process_lesson(api, lesson_content, output_filepath)
            except Exception as e:
                print(f"  !!! FAILED to process Lesson {lesson_num}: {e}")

if __name__ == '__main__':
    main()
