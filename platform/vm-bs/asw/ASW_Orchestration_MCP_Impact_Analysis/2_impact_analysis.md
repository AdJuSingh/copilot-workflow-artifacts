


# Instructions for Impact Analysis


Given {updated_requirements} with respect to the workspace, perform impact analysis.
Workspace is {codebase_for_edit}.
Note: call the mcp with user given requirements itself.
Run the mcp server Impact_analysis_agent and pass the parameter {updated_requirements} and wait for the mcp_tools' output. 
MCP tool  Impact Analysis agent will return the detailed workspace level impact analysis , store it in {impact_analysis}
display the impact analysis agent's output 
Save the Impact Analysis output as a Readable, crisp and clear  Impact_analysis_{component}_{timestamp}.md file without hallucinations in the workspace
# Next Step

After the impact analysis is complete, ask for user verification and feedback, then load the 2.5_Memory.md and fetch the relevant context from the memory.md file and store it in {memory_context} escpecially check the user_feedback section in all the indexes, show the fetched memory context to the user, then load the 3_Implementation_plan and continue.