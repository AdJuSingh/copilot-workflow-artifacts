
This 1_Knowledge_graph.md defines the entire workflow for creation of an RDF Knowledge Graph

Create a comprehensive system-level Knowledge Graph for an Automotive Embedded Software codebase based on C/C++ with the aim of effectively performing system-level impact analysis.


**CRITICAL RULES:**
- Create RDF-based .jsonld file named {SystemName}_Knowledge_Graph.jsonld (NOT .json)
- System-level coverage of ALL components in {codebase_for_edit} - never component-specific
- Don't hallucinate - only include information found in actual files
- Workspace structure: src/rbc.cpp/.hpp (source files + subdirectories) and tst/gtest (unit tests)


## METHODOLOGY:
1. **Scan ALL files**: Every .hpp/.h file in the workspace recursively + corresponding .cpp and test files
2. **Extract requirements**: From @unit/@endunit sections in header files
3. **Map traceability**: Requirements → .hpp → .cpp → test files → classes/methods/functions
4. **Include code snippets**: Small snippets with accurate descriptions for key components


## REQUIRED JSON-LD STRUCTURE:
```json
{
"@context": {
    "ex": "http://example.org/ontology/",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "satisfiedBy": {"@type": "@id"},
    "implements": {"@type": "@id"},
    "dependsOn": {"@type": "@id"},
    "calls": {"@type": "@id"},
    "definedIn": {"@type": "@id"},
    "testedBy": {"@type": "@id"},
    "hasFunction": {"@type": "@id"},
    "hasClass": {"@type": "@id"},
    "hasMethod": {"@type": "@id"},
    "hasSubsystem": {"@type": "@id"}
},
"@graph": [
    // System Entity
    {
    "@id": "ex:{SystemName}_System",
    "@type": "ex:AutomotiveSystem",
    "hasSubsystem": ["ex:Subsystem1", "ex:Subsystem2"],
    "satisfiedBy": "ex:{SystemName}_Functional_Requirements"
    },
    // Requirements from @unit sections
    {
    "@id": "ex:{RequirementName}_Requirements",
    "@type": "ex:FunctionalRequirement",
    "ex:requirementText": "{Extracted from @unit/@endunit}"
    },
    // Files with traceability
    {
    "@id": "ex:{filename}_hpp",
    "@type": "ex:HeaderFile", 
    "ex:filePath": "{relative_path}",
    "hasClass": "ex:{ClassName}_Class",
    "testedBy": "ex:test_{filename}_cpp"
    },
    // Classes with code snippets
    {
    "@id": "ex:{ClassName}_Class",
    "@type": "ex:CppClass",
    "definedIn": "ex:{filename}_hpp",
    "hasMethod": ["ex:{method1}", "ex:{method2}"],
    "ex:codeSnippet": "{Actual class definition}"
    },
    // Functions with signatures
    {
    "@id": "ex:{functionName}_function",
    "@type": "ex:Function",
    "ex:signature": "{Complete function signature}",
    "implements": "ex:{Related_Requirement}",
    "calls": ["ex:{called_function1}"]
    },
    // Test files
    {
    "@id": "ex:test_{filename}_cpp",
    "@type": "ex:TestFile",
    "testedBy": "ex:{source_file}",
    "hasTestCase": ["ex:{TestCase1}"]
    }
]
}
```


## ENTITY NAMING:
- Files: `{filename}_hpp`, `{filename}_cpp`
- Classes: `{ClassName}_Class`
- Functions: `{functionName}_function`
- Tests: `test_{filename}_cpp`
- Requirements: `{RequirementName}_Requirements`


## EXECUTION:
1. Analyze ALL .hpp files in the workspace (not just key files)
2. Extract requirements from @unit sections in headers
3. Map: Requirements→.hpp→.cpp→test file→classes/methods/functions
4. Build a complete system-level RDF graph with accurate code snippets
5. Output: {SystemName}_Knowledge_Graph.jsonld


After Knowledge_Graph.jsonld is complete, load the 2_Requirement_elicitation_impact_analysis.md and continue the workflow
