import asyncio
import os
import shutil
from pathlib import Path
import subprocess # For running Manim CLI

# This base directory path assumes manim_service.py is in app/backend/services/
# and the static content is in app/backend/static_content/manim_videos/
# Adjust if your project structure is different or use an absolute path from settings.
MANIM_OUTPUT_BASE_DIR = Path(__file__).resolve().parent.parent / "static_content" / "manim_videos"

# Ensure the base output directory exists upon module load
MANIM_OUTPUT_BASE_DIR.mkdir(parents=True, exist_ok=True)

# Helper to run subprocess asynchronously
async def run_manim_subprocess_async(command_list: list[str], cwd: Path) -> tuple[int, str, str]:
    """Runs a subprocess asynchronously and returns its exit code, stdout, and stderr."""
    print(f"[Manim Service] Executing command: {' '.join(command_list)} in CWD: {cwd}")
    process = await asyncio.create_subprocess_exec(
        *command_list,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=str(cwd) # Manim often works best when CWD is where its outputs go or where scripts are
    )
    stdout, stderr = await process.communicate()
    
    stdout_decoded = stdout.decode().strip()
    stderr_decoded = stderr.decode().strip()

    if stdout_decoded:
        print(f"[Manim Service] Subprocess STDOUT:\n{stdout_decoded}")
    # Always print stderr, even if empty, for consistency in logs, or only if non-empty
    if stderr_decoded: 
        print(f"[Manim Service] Full Subprocess STDERR for job {cwd.name}:\n{stderr_decoded}")
    else:
        print(f"[Manim Service] Subprocess STDERR for job {cwd.name}: <empty>")
    
    return process.returncode, stdout_decoded, stderr_decoded

async def execute_manim_code(job_id: str, manim_code: str, scene_name: str = "ConfusedAssistant") -> tuple[str | None, str | None]:
    """
    Executes Manim code by saving it to a file and running the Manim CLI.
    """
    print(f"[Manim Service] Real execution called for job {job_id} with scene '{scene_name}'.")

    job_dir = MANIM_OUTPUT_BASE_DIR / job_id
    script_dir = job_dir / "script" # Place script in its own subfolder
    script_dir.mkdir(parents=True, exist_ok=True)
    manim_script_path = script_dir / "generated_scene.py"

    # --- Clean the Manim code from Markdown backticks --- 
    cleaned_code = manim_code.strip()
    if cleaned_code.startswith("```python"):
        cleaned_code = cleaned_code[len("```python"):].lstrip()
    elif cleaned_code.startswith("```"):
        cleaned_code = cleaned_code[len("```"):].lstrip()
        
    if cleaned_code.endswith("```"):
        cleaned_code = cleaned_code[:-len("```")]
    cleaned_code = cleaned_code.strip() # Final strip for any residual newlines around the actual code
    # --- End cleaning ---

    if not cleaned_code:
        error_msg = "Cleaned Manim code is empty after stripping backticks."
        print(f"[Manim Service] {error_msg}")
        return None, error_msg

    try:
        with open(manim_script_path, "w", encoding='utf-8') as f:
            f.write(cleaned_code)
        print(f"[Manim Service] Cleaned Manim code saved to: {manim_script_path}")
        # print(f"[Manim Service] Cleaned code preview (first 500 chars):\n{cleaned_code[:500]}...")
    except Exception as e:
        error_msg = f"Failed to save Manim script: {e}"
        print(f"[Manim Service] {error_msg}")
        return None, error_msg

    # Manim will create its media directory relative to where it's run or via --media_dir
    # We will set media_dir to be inside our job_id folder for organization.
    # Manim typically creates: media_dir/videos/script_name_no_ext/resolution/SceneName.mp4
    # We want media_dir to be just job_dir, so Manim creates job_dir/media/...
    
    # Quality: -ql (low), -qm (medium), -qh (high), -qk (4k)
    # For dev, -ql (480p15) is fastest. For production, -qh (1080p60) or -qk (2160p60)
    quality_flag = "-ql"
    # Expected output structure based on Manim's default naming with media_dir set
    # e.g., job_dir/media/videos/generated_scene/480p15/ConfusedAssistant.mp4
    # The relative path for the URL will be job_id/media/videos/generated_scene/480p15/ConfusedAssistant.mp4
    # Manim uses the Python script's filename (without .py) as a subdirectory.
    script_filename_no_ext = manim_script_path.stem # e.g., "generated_scene"
    resolution_dir_name = "480p15" # This corresponds to -ql

    # The path Manim will create, relative to MANIM_OUTPUT_BASE_DIR
    relative_video_output_dir_for_url = Path(job_id) / "videos" / script_filename_no_ext / resolution_dir_name
    expected_video_filename = f"{scene_name}.mp4"
    expected_relative_video_path_for_url = relative_video_output_dir_for_url / expected_video_filename

    # Command to execute Manim
    # Ensure 'python' and 'manim' are correctly available in the environment PATH
    # Using "python -m manim" is often more robust.
    cmd = [
        "python", "-m", "manim",
        "render", # render subcommand for Manim Community v0.18+
        str(manim_script_path.resolve()), # Absolute path to script
        scene_name,                     # Scene class name to render
        quality_flag,                   # Quality flag
        "--media_dir", str(job_dir.resolve()), # Output media to job-specific dir
        # "--output_file", expected_video_filename, # Optional: if you want to enforce output filename
        # "--format", "mp4", # Usually default, but can be explicit
        # "--progress_bar", "none" # To reduce console noise from Manim if desired
    ]

    try:
        print(f"[Manim Service] About to run Manim for job {job_id} on scene '{scene_name}'...")
        # Manim commands often work best when CWD is the script's directory or project root.
        # Setting CWD to script_dir or job_dir might be beneficial.
        return_code, stdout_str, stderr_str = await run_manim_subprocess_async(cmd, cwd=script_dir)

        if return_code != 0:
            error_msg = f"Manim execution failed with code {return_code}. STDERR: {stderr_str[:1000]}..." # Increased length for better error visibility
            print(f"[Manim Service] {error_msg}")
            return None, error_msg

        # Add a small delay to allow filesystem to catch up after Manim process exits
        await asyncio.sleep(0.2) 

        # Verify the output file was created
        absolute_expected_video_path = MANIM_OUTPUT_BASE_DIR / expected_relative_video_path_for_url
        print(f"[Manim Service] Checking for primary output file: {absolute_expected_video_path}")
        if absolute_expected_video_path.exists() and absolute_expected_video_path.is_file():
            print(f"[Manim Service] Manim execution successful. Video created: {absolute_expected_video_path}")
            return str(expected_relative_video_path_for_url), None # Return the relative path for URL
        else:
            print(f"[Manim Service] Primary output file NOT found at {absolute_expected_video_path}.")
            # Fallback: Search for *any* .mp4 in the job_dir structure
            search_path = MANIM_OUTPUT_BASE_DIR / job_id / "videos" / script_filename_no_ext / resolution_dir_name
            print(f"[Manim Service] Fallback: Attempting to search for *.mp4 in {search_path}")
            found_videos = list(search_path.glob(f"*.mp4")) # Search for any mp4 in the scene's quality folder
            print(f"[Manim Service] Fallback: Found video files by glob: {found_videos}")
            
            if found_videos:
                target_video = None
                # Prefer a file that contains the scene_name, case-insensitively
                for vid in found_videos:
                    if scene_name.lower() in vid.name.lower():
                        target_video = vid
                        print(f"[Manim Service] Fallback: Matched scene name with {vid.name}")
                        break
                if not target_video: # If no name match, take the first one found
                    target_video = found_videos[0]
                    print(f"[Manim Service] Fallback: No direct scene name match, using first found: {target_video.name}")

                relative_found_path = target_video.relative_to(MANIM_OUTPUT_BASE_DIR)
                print(f"[Manim Service] Fallback: Using video at {target_video}. Relative path: {relative_found_path}")
                return str(relative_found_path), None
            else:
                error_msg = f"Manim executed (code 0), but output file not found at {absolute_expected_video_path} AND no *.mp4 files found in fallback search path {search_path}. STDERR: {stderr_str[:500]}... STDOUT: {stdout_str[:500]}..."
                print(f"[Manim Service] {error_msg}")
                return None, error_msg # If still not found

    except FileNotFoundError as fnf_error: # Catch if `python`
        error_msg = f"Manim command execution error (FileNotFoundError): {fnf_error}. Is 'python' and Manim installed and in PATH?"
        print(f"[Manim Service] {error_msg}")
        return None, error_msg
    except Exception as e: # Catch any other exceptions
        error_msg = f"An unexpected error occurred during Manim execution: {e}"
        print(f"[Manim Service] {error_msg}")
        import traceback
        traceback.print_exc()
        return None, error_msg