
# Important: This document acts as the sole reference for the Entire Application Software Development Workflow
## Important: don't summarize the contents of the instruction file in the beginning and don't display the same to the user - the user should only receive a clear step-by-step structured execution of the workflow defined. Don't show Introduction, Workflow Overview, key features, or anything like that.
# Important: Follow the instruction files as it is. Don't refer Copilot Short term memory or Long Term memory
# Important: Never modify or corrupt this file
# LLM: Claude Sonnet 4
# Keep the outputs really concise and to the point, don't write summaries, write only checklists
# Temperature = 0.3, Top-p = 0.4, total token output limit=3000.


## This instruction file defines a 5-step workflow for modification of an existing Automotive Embedded software workspace with updated requirements this is the main orchestrator instruction file that will call other instruction files in sequence to achieve the desired modifications in the codebase based on updated requirements provided by the user.



    # Step 1: Take the updated_requirement from user and do requirements elicicitation as in 1_Requirements_elicitation.md 

    # Step 2: Impact Analysis The specific instructions for requirements fetching and impact analysis are present in 2_impact_analysis.md

    # Step 2.5: [Fetch relevant context from memory]: Read the relevant context from 2.5_memory.md with respect to {updated_requirements} to get any additional information about the codebase or requirements. Display the fetched {memory_context}.

    # Step 3: [Implementation Plan] Implementation planning in 3_Implementation_plan.md

    # Step 4: [Use the Implementation plan for codebase modification with user validation] The specific instructions for modification of the workspace are present in 4_Codebase_modification.md

    # Step 5: [Run Unit Test] & [CTTCodeCoverage] After making the necessary modifications, load the 5_Run_Unit_Tests_and_update_memory.md and follow the instructions set there.

    # Step 5.5: Update the Memory.md with the summary [Update_requirements, Files modified, User feedback summary]




