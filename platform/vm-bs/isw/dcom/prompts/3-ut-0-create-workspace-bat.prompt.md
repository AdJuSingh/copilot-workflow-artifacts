---
agent: agent
model: Claude Sonnet 4.5
description: 'BSW Test Compilation Agent - Initial phase: Create project structure and batch files'
tools: ['editFiles', 'search', 'runCommands', 'runTasks', 'usages', 'extensions', 'codebase', 'createFile']
---

# Prompt: Generate 4 Batch Files for Cantata Unit Testing Workflow

## STEP 0 - User Input (MANDATORY FIRST)

**USER MUST PROVIDE:** Full path to the source .c file
- Example: `C:\Users\RGA8HC\Downloads\CHRYSLER_IPB\rb\as\ms\core\app\dcom\RBAPLCust\src\RBAPLCUST_Module.c`

## STEP 1 - Create UT Folder Structure (AUTOMATIC)

**YOU MUST CREATE:**

1. **Extract filename without extension from provided path**
   - Example: `RBAPLCUST_Module.c` → `RBAPLCUST_Module`

2. **Determine UT folder name:** `UT_<filename>`
   - Example: `RBAPLCUST_Module.c` → `UT_RBAPLCUST_Module`

3. **Determine UT folder location:** One level up from the source file directory
   - Example: If file is `C:\...\RBAPLCust\src\RBAPLCUST_Module.c`
   - Create folder at: `C:\...\RBAPLCust\UT_RBAPLCUST_Module`

4. **Create folder structure:**
```
<ParentDir>/
├── UT_<filename>/
│   ├── build_test.bat          (to be created)
│   ├── compile_project.bat     (to be created)
│   ├── generate_test.bat       (to be created)
│   ├── generate_test_summary.bat (to be created)
│   ├── ipg.cop
│   └── src/
│       └── <filename>.c        (COPY from user's provided path)
```

5. **Copy source file:**
   - Copy the provided .c file into `UT_<filename>\src\` folder

6. **Create ipg.cop file**

## Create ipg.cop file inside the UT_xxx folder
#
# Cantata Project-Level Options
#
# The options set in this file will be inherited by each test in the project.
#
# WARNING: Do not alter this file manually.
#
```cop
#tool.use=true
#tool.tests=Cantata
#tool.version=2
"--analyse"
"--ci:--instr:stmt;func;rel;loop;call;decn;log;"
"--parse:--line_directives"
"--parse:-W2"
"--sm:--call_seq_code"
"--comp:x86-Win32-gcc4.8.1"

#User Section
```
## STEP 2 - Environment Selection (MANDATORY)

**The @aeee agent will present buttons for environment selection.**

Click one of the buttons to select your AEEE environment:
- **AEEE-PRO Environment** - Professional environment
- **AEEE-ECO Environment** - Economy environment (default: aeee_eco/2020.1.2)

**After environment selection, IMMEDIATELY create the 4 batch files in the UT folder - DO NOT ask for any additional information.**

## STEP 3 - Automatic Configuration

After environment is selected, automatically:

1. **Detect AEEE Version**: 
   - Scan `C:\toolbase\aeee_eco` (for ECO) or `C:\toolbase\aeee_pro` (for PRO)
   - Find the latest version directory (e.g., `2020.1.2`, `2023.1.0`)
   - Use this version in `call texec` command

2. **Check Existing Files in UT folder**:
   - Look for `.bat` files in `UT_<filename>` folder
   - Files: `compile_project.bat`, `generate_test.bat`, `build_test.bat`, `generate_test_summary.bat`
   - If exist: UPDATE the `call texec` line with new environment version
   - If not exist: CREATE new files using templates below

3. **Create 4 Batch Files in UT_<filename> folder** using these exact templates (only replace `call texec aeee_eco/2020.1.2` with detected version):

### File 1: compile_project.bat
```bat
@echo off
set PROJECT_PATH=%1

cd %PROJECT_PATH%

echo Step 1: Initialize Cantata environment (command-line only)
call texec aeee_eco/2020.1.2
cd %PROJECT_PATH%
if not exist "..\Debug\objects" mkdir "..\Debug\objects" 
if not exist "..\Debug\csi" mkdir "..\Debug\csi" 

echo Step 2: Compile all source files
set SOURCE_FILE=..\src\%2.c
echo Compiling %SOURCE_FILE%...
set OBJECT_FILE=%~n2.o
echo Object File: %OBJECT_FILE%
cppccd.exe -F %PROJECT_PATH%\ipg.cop --analyse --parse:--line_directives --parse:-W2 --sm:--call_seq_code --ci:--static_info_file:%PROJECT_PATH% --comp:x86-Win32-gcc4.8.1 --objfile:%OBJECT_FILE% gcc -o %OBJECT_FILE% -c %SOURCE_FILE% -I..\src -Iapi\stubs

echo ===COMPILE_DONE===
```

### File 2: generate_test.bat
```bat
@echo off
set PROJECT_PATH=%1
set WORKSPACE_PATH=%PROJECT_PATH%/../
if "%PROJECT_PATH%"=="" (
    echo Error: PROJECT_PATH not provided
    exit /b 1
)

echo Step 1: Initialize Cantata environment
call texec aeee_eco/2020.1.2

echo Step 2: Generate test scripts
%UBK_PRODUCT% -application com.ipl.products.eclipse.cantpp.testscript.AutoTestGenerator -noSplash -data %WORKSPACE_PATH% sourceDirectory=%PROJECT_PATH% makefileEnabled=false coverageRuleset="Report all Metrics" overwrite=true

echo Finished generating test scripts!
```

### File 3: build_test.bat
```bat
@echo off
setlocal enabledelayedexpansion

set WORKSPACE_PATH=%~dp0
set PROJECT_PATH=%1
set C_FILE=%2

if "%PROJECT_PATH%"=="" (
    echo Error: PROJECT_PATH not provided
    exit /b 1
)

if "%C_FILE%"=="" (
    echo Error: C_FILE not provided
    exit /b 1
)

echo Step 1: Initialize Cantata environment
call texec aeee_eco/2020.1.2
if errorlevel 1 goto :error

set TEST_PATH=%PROJECT_PATH%\Cantata\tests\atest_%C_FILE%

echo Step 2: Verify test path exists
if not exist "%TEST_PATH%" (
    echo Error: Test path does not exist: %TEST_PATH%
    exit /b 1
)

cd /d %TEST_PATH%

echo Step 3: Compile test source
set OBJECT_FILE=%TEST_PATH%\atest_%C_FILE%.o
set SOURCE_FILE=%TEST_PATH%\atest_%C_FILE%.c
cppccd.exe -F %TEST_PATH%\ipg.cop --analyse --parse:--line_directives --parse:-W2 --sm:--call_seq_code --comp:x86-Win32-gcc4.8.1 --ci:--static_info_file:%TEST_PATH%\ --objfile:%OBJECT_FILE% gcc -o %OBJECT_FILE% -c %SOURCE_FILE% -I..\..\..\api\stubs -I..\..\..\src -Ic:\toolbase\ecl_cantata\9.0.0\eclipse\inc
if errorlevel 1 goto :error

echo Step 4: Link executable
set TEST_OBJECT_FILE=%TEST_PATH%\atest_%C_FILE%.o
set SOURCE_OBJECT_FILE=%PROJECT_PATH%\%C_FILE%.o
set EXECUTABLE_FILE=%TEST_PATH%\atest_%C_FILE%.exe
gcc.exe %TEST_OBJECT_FILE% %SOURCE_OBJECT_FILE% -o %EXECUTABLE_FILE% -I%TB_ECL_CANTATA_HOME%\eclipse\inc -L%TB_ECL_CANTATA_HOME%\eclipse\libs\lib-x86-Win32-gcc4.8.1 -lcantpp
if errorlevel 1 goto :error

echo Step 5: Run tests
call %EXECUTABLE_FILE%
if errorlevel 1 goto :error

echo All steps completed successfully!
exit /b 0

:error
echo Error occurred during execution
exit /b 1
```

### File 4: generate_test_summary.bat
```bat

set PROJECT_PATH=%1
set WORKSPACE_PATH=%PROJECT_PATH%/../
echo Step 1: Initialize Cantata environment (command-line only)
call texec aeee_eco/2020.1.2

echo Test summary generation completed.
%UBK_PRODUCT% -application com.ipl.products.eclipse.cantpp.cdt.TestReportGenerator -data %WORKSPACE_PATH% %PROJECT_PATH% HTML_DETAILED_REPORT
```

**Important**: Replace ALL occurrences of `call texec aeee_eco/2020.1.2` with the detected version:
- For AEEE-ECO: `call texec aeee_eco/X.X.X` (e.g., `aeee_eco/2020.1.2`)
- For AEEE-PRO: `call texec aeee_pro/X.X.X` (e.g., `aeee_pro/2023.1.0`)

---

### File 5: tpaFileGenerator.pl: 
```pl
#!/usr/bin/perl
use strict;
use warnings;
use XML::LibXML;
use Time::Piece;
use POSIX qw(strftime);
use XML::Simple;
use Data::Dumper;
use File::Find;
use File::Basename;
use Data::Dumper;

my $input_xml = $ARGV[0];
my $output_tpa= $ARGV[1];
my $chnageSetargv = $ARGV[2];
my $workItemno = $ARGV[3];
my $folderpath = $ARGV[4];

die "Error: Invalid Arguments - Expected 5 parameters\n" if @ARGV < 5;

# Validate input file
unless (-f $input_xml) {
    die "Error: XML file not found: $input_xml\n";
}

# Validate folder path
unless (-d $folderpath) {
    die "Error: Folder path not found: $folderpath\n";
}

print "\nInput xml file: $input_xml \n";
my $data_hash_ref = Read_XML ($input_xml);
createExclusiontpaFile();
my @fileList;
find({ wanted => \&process_file, no_chdir => 1 }, $folderpath);
Write_to_TPA($data_hash_ref);

print "\nScript completed successfully\n";
exit 0;

################################################################################
sub Read_XML {
    my $xml_file = shift;
    
    my ($xml, $xml_data, $xml_req_data);
    
    # create object
    $xml = new XML::Simple;
    
    # read XML file
    $xml_data = $xml->XMLin($xml_file);
    
    $xml_req_data = Get_Req_data($xml_data);
    undef $xml_data;
    return $xml_req_data;
}
################################################################################
sub Get_Req_data {
    my $xml_hash_ref = shift;
    
    my $months_hash = {
                      'January'  => '01',
                      'February' => '02',
                      'March'    => '03',
                      'April'    => '04',
                      'May'      => '05',
                      'June'     => '06',
                      'July'     => '07',
                      'August'   => '08',
                      'September'=> '09',
                      'October'  => '10',
                      'November' => '11',
                      'December' => '12'
                      };
    my $req_data_hashref;	
    foreach my $c_file (keys %{$xml_hash_ref->{'coverageReport'}{'srcFile'}}){
        $req_data_hashref->{$c_file}{'C_name'} = $c_file;
		
        my @keyList = keys %{$xml_hash_ref->{'coverageReport'}{'srcFile'}};		
		if (grep { $_ !~ /\.c$/ } @keyList) {
		    if (!defined $xml_hash_ref->{'coverageReport'}{'srcFile'}{'name'} || $xml_hash_ref->{'coverageReport'}{'srcFile'}{'name'} eq "") {
			    $req_data_hashref->{$c_file}{'C0'} = $xml_hash_ref->{'coverageReport'}{'srcFile'}{$c_file}{'fileCoverage'}{'coverageAchieved'}{'statement'};
				$req_data_hashref->{$c_file}{'C1'} = $xml_hash_ref->{'coverageReport'}{'srcFile'}{$c_file}{'fileCoverage'}{'coverageAchieved'}{'decision'};
				$req_data_hashref->{$c_file}{'MC/DC'} = $xml_hash_ref->{'coverageReport'}{'srcFile'}{$c_file}{'fileCoverage'}{'coverageAchieved'}{'booleanOperandEffectivenessUnique'};
			} else {
			    $req_data_hashref->{$c_file}{'C0'} = $xml_hash_ref->{'coverageReport'}{'srcFile'}{'fileCoverage'}{'coverageAchieved'}{'statement'}; 
                $req_data_hashref->{$c_file}{'C1'} = $xml_hash_ref->{'coverageReport'}{'srcFile'}{'fileCoverage'}{'coverageAchieved'}{'decision'};
				$req_data_hashref->{$c_file}{'MC/DC'} = $xml_hash_ref->{'coverageReport'}{'srcFile'}{'fileCoverage'}{'coverageAchieved'}{'booleanOperandEffectivenessUnique'};
			    $req_data_hashref->{$c_file}{'C_name'} = $xml_hash_ref->{'coverageReport'}{'srcFile'}{'name'};
			}		    
		} else {
		    $req_data_hashref->{$c_file}{'C0'} = $xml_hash_ref->{'coverageReport'}{'srcFile'}{$c_file}{'fileCoverage'}{'coverageAchieved'}{'statement'};
            $req_data_hashref->{$c_file}{'C1'} = $xml_hash_ref->{'coverageReport'}{'srcFile'}{$c_file}{'fileCoverage'}{'coverageAchieved'}{'decision'};
			$req_data_hashref->{$c_file}{'MC/DC'} = $xml_hash_ref->{'coverageReport'}{'srcFile'}{$c_file}{'fileCoverage'}{'coverageAchieved'}{'booleanOperandEffectivenessUnique'};
		}
		my @data;
		if (ref($xml_hash_ref->{'testResults'}{'testScript'}) eq 'ARRAY') {
		    @data = @{$xml_hash_ref->{'testResults'}{'testScript'}};
		} else {
		    push @data, $xml_hash_ref->{'testResults'}{'testScript'};
		}
		
        foreach my $each_test (@data){
            my $temp_c_file = $each_test->{'info'}{'testScriptName'};	
            #$temp_c_file =~ s/test_//;		
			#$temp_c_file =~ s/^a//; 	
            next if ($req_data_hashref->{$c_file}{'C_name'} =~ /\.h$/);
            
            # Skip if testScriptName is not defined
            next unless defined $temp_c_file;
            
			$temp_c_file = $temp_c_file.'.c';	
            
            my $actual_file_name = $req_data_hashref->{$c_file}{'C_name'};
            my $dummy_file_name = $temp_c_file;
            
            # Skip undefined values
            next unless (defined $actual_file_name && defined $dummy_file_name);
		        
			# Simple comparison - match if filenames are equal
			if ($dummy_file_name eq $actual_file_name) {   
                if ($each_test->{'summary'}{'status'} =~ /passed/i){
                    $req_data_hashref->{$c_file}{'Verdict'} = 'Passed';
                }
                elsif ($each_test->{'summary'}{'status'} =~ /failed/i) {
                    $req_data_hashref->{$c_file}{'Verdict'} = 'Failed';
                }
                elsif ($each_test->{'summary'}{'status'} =~ /Undefined/i) {
                    $req_data_hashref->{$c_file}{'Verdict'} = 'Undefined';
                }
                else {
                    $req_data_hashref->{$c_file}{'Verdict'} = 'NotApplicable';
                }
                $each_test->{'info'}{'testScriptDescription'} =~ s/\s+//g;
				
                if ($each_test->{'info'}{'testScriptDescription'} =~ /\=(.*V\d+\.\d+)\=+.*\=+TestStarted\:(.*)\=/i){				    
                    my $tool_data = $1;
                    my $tested_date =$2;
                    if ($tool_data =~ /(.*)v(\d+\.\d+)/i){
                        $req_data_hashref->{$c_file}{'Toolname'} = $1;
                        $req_data_hashref->{$c_file}{'Version'} = $2;
                    }
                    
                    if($tested_date =~ /.*(\w\w\w)(\d\d)(\d\d\:\d\d\:\d\d)(\d+)/){
                        my $month = $1;
                        foreach my $mnth (keys %{$months_hash}){
                            if ($mnth =~ /$month/i){
                                $month = $months_hash->{$mnth};
                                last;
                            }
                        }
                        $req_data_hashref->{$c_file}{'TestedDate'} = $4.'-'.$month.'-'.$2.'T'.$3.'Z';
                    }
                    else {
                        $req_data_hashref->{$c_file}{'TestedDate'} = $tested_date;
                    }
                } else {
				    
				}
                last;
            }
        }
    }    
    return $req_data_hashref;
}
################################################################################


sub WriteToXml {
    my ($actionDoc, $metaDataRoot) = @_;	
	my ($action,$fileAdd,$csNameRef,$fileMatcher,$action1,$assoAdd,$sourceFileMatcher,$targetFileMatcher,$associationType); 
	foreach my $c_file (@fileList) {
	    $action = $actionDoc->createElement( "Action" );
		$metaDataRoot->appendChild($action);
		
		$fileAdd = $actionDoc->createElement( "FileAdd" );
		$action->appendChild($fileAdd);
			
		$csNameRef = $actionDoc->createElement( "CsNameRef" );
		$csNameRef->appendTextNode($chnageSetargv);
		$fileAdd->appendChild($csNameRef);
			
		$fileMatcher = $actionDoc->createElement( "FileMatcher" );
		my $cFile1 = $c_file;
		#$cFile1 =~ s/\.c/.tpa/;	
		$fileMatcher->appendTextNode('**/'.$cFile1);
		$fileAdd->appendChild($fileMatcher);
		
		$action1 = $actionDoc->createElement( "Action" );
		$metaDataRoot->appendChild($action1);
			
		$assoAdd = $actionDoc->createElement( "AssoAdd" );
		$action1->appendChild($assoAdd);
			
		$sourceFileMatcher = $actionDoc->createElement( "SourceFileMatcher" );
		$sourceFileMatcher->appendTextNode('**/'.$c_file);
		$assoAdd->appendChild($sourceFileMatcher);
		
		$targetFileMatcher = $actionDoc->createElement( "TargetFileMatcher" );
		$targetFileMatcher->appendTextNode("testcase.tpa");
		$assoAdd->appendChild($targetFileMatcher);
		
		$associationType = $actionDoc->createElement( "AssociationType" );
		$associationType->appendTextNode("unit_test_spec_result");
		$assoAdd->appendChild($associationType);
	}	
	
}
 sub createExclusiontpaFile{

 my ($doc, $root, $UUT, $test, $test_notnecessary,$exclusion_category,$exclusion_comment,$decidedby,$user_ID);
		 $doc = 	XML::LibXML::Document->new('1.0', 'utf-8');
         $root = $doc->createElement("TestProcessAttributes");
         $root->setAttribute( 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation', "http://abt-syseng.de.bosch.com/TestProcessAttributes/TestProcessAttributes_2_3.xsd");

		 $UUT = $doc->createElement( "UnitUnderTest" );
		 $UUT->appendTextNode("TestScripts");
         $root->appendChild($UUT);
		
		 $test = $doc->createElement( "Test" );
        $root->appendChild($test);
		
		 $test_notnecessary = $doc->createElement( "TestNotNecessary" );
		$test->appendChild($test_notnecessary);
		
		$exclusion_category = $doc->createElement( "ExclusionCategory" );
		 $exclusion_category->appendTextNode("NoCode");
		 $test_notnecessary->appendChild($exclusion_category);
		
		 $exclusion_comment = $doc->createElement( "ExclusionComment" );
		 $exclusion_comment->appendTextNode("TestCase");
		 $test_notnecessary->appendChild($exclusion_comment);
		
		 $decidedby = $doc->createElement( "DecidedBy" );
		 
		 $decidedby->appendTextNode($ENV{'USERNAME'});
		$test_notnecessary->appendChild($decidedby);
		
		 $doc->setDocumentElement($root);
		 $doc->toFile($output_tpa."\\testcase.tpa", 1);
		
}
################################################################################
sub Write_to_TPA {
    my $data_hash_ref = shift;
    
	#my $tpa_dir = 'D:\TPA_Files';
    
    unless (-d $output_tpa){
        unless( mkdir $output_tpa , 0777 ) {
            print "Unable to create directory $output_tpa... using default directory\n";
            $output_tpa = 'C:\temp';
        }
    }
    
    
	my ( $actionDoc, $metaDataRoot, $changesets, $changeset, $csName,$workItemNo,$action,$fileAdd,$csNameRef,$fileMatcher,$action1,$assoAdd,$sourceFileMatcher,$targetFileMatcher,$associationType); 
	
	$actionDoc = XML::LibXML::Document->new('1.0', 'utf-8');
	$metaDataRoot = $actionDoc->createElement("MetaDataTool");
	$metaDataRoot->setAttribute( 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation', "MDT_1.0.xsd");	   
	
	$changesets = $actionDoc->createElement( "ChangeSets" );
	$metaDataRoot->appendChild($changesets);
  
	$changeset = $actionDoc->createElement( "Changeset" );
	$changesets->appendChild($changeset);
	
	$csName = $actionDoc->createElement( "CsName" );
	$csName->appendTextNode($chnageSetargv);
	$changeset->appendChild($csName);
		
	$workItemNo = $actionDoc->createElement( "WorkItemNo" );
	$workItemNo->appendTextNode($workItemno);
	$changeset->appendChild($workItemNo);
		
	foreach my $c_file (keys %{$data_hash_ref}){
	next if ($data_hash_ref->{$c_file}{'C_name'} =~ /\.h$/);
	$action = $actionDoc->createElement( "Action" );
	$metaDataRoot->appendChild($action);
		
	$fileAdd = $actionDoc->createElement( "FileAdd" );
	$action->appendChild($fileAdd);
		
	$csNameRef = $actionDoc->createElement( "CsNameRef" );
	$csNameRef->appendTextNode($chnageSetargv);
	$fileAdd->appendChild($csNameRef);
		
	$fileMatcher = $actionDoc->createElement( "FileMatcher" );
	my $cFile1 = $data_hash_ref->{$c_file}{'C_name'};
	$cFile1 =~ s/\.c/.tpa/;	
	$fileMatcher->appendTextNode('**/'.$cFile1);
	$fileAdd->appendChild($fileMatcher);
	
	$action1 = $actionDoc->createElement( "Action" );
	$metaDataRoot->appendChild($action1);
		
	$assoAdd = $actionDoc->createElement( "AssoAdd" );
	$action1->appendChild($assoAdd);
		
	$sourceFileMatcher = $actionDoc->createElement( "SourceFileMatcher" );
	$sourceFileMatcher->appendTextNode('**/'.$data_hash_ref->{$c_file}{'C_name'});
	$assoAdd->appendChild($sourceFileMatcher);
	
	$targetFileMatcher = $actionDoc->createElement( "TargetFileMatcher" );
	$targetFileMatcher->appendTextNode('**/'.$cFile1);
	$assoAdd->appendChild($targetFileMatcher);
	
	$associationType = $actionDoc->createElement( "AssociationType" );
	$associationType->appendTextNode("unit_test_spec_result");
	$assoAdd->appendChild($associationType);
	
		}
	
	WriteToXml($actionDoc, $metaDataRoot);
	
	$actionDoc->setDocumentElement($metaDataRoot);
	$actionDoc->toFile($output_tpa."\\mdt_action.xml", 1);
	
	
	my ($doc, $root, $UUT, $TestStatus, $Test, $user_ID, $test_result, $test_verdict, $test, $tested_part);
    my ($test_value, $test_coverage, $test_percentage, $test_metric_name, $Execution_time, $Tool_used, $Tool_version);
    my ($testresult, $test_tool, $testpart);
    
	
    
	foreach my $c_file (keys %{$data_hash_ref}){
        next if ($data_hash_ref->{$c_file}{'C_name'} =~ /\.h$/);
        $doc = XML::LibXML::Document->new('1.0', 'utf-8');
        $root = $doc->createElement("TestProcessAttributes");
        $root->setAttribute( 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation', "http://abt-syseng.de.bosch.com/TestProcessAttributes/TestProcessAttributes_2_3.xsd");
        
        $UUT = $doc->createElement( "UnitUnderTest" );
	      $UUT->appendTextNode($data_hash_ref->{$c_file}{'C_name'});
        $root->appendChild($UUT);
        
        $test = $doc->createElement( "Test" );
        $root->appendChild($test);
        
        $test_result = $doc->createElement( "TestResult" );
		    $test->appendChild($test_result);
		    
		    $user_ID = $doc->createElement("NTUserID");
        $user_ID->appendTextNode($ENV{'USERNAME'});
			  $test_result->appendChild($user_ID);
			  
			  $Execution_time = $doc->createElement("ExecutionDate");
        $Execution_time->appendTextNode($data_hash_ref->{$c_file}{'TestedDate'});
			  $test_result->appendChild($Execution_time);
			  
			  $test_tool = $doc->createElement( "Tool" );
		    $test_result->appendChild($test_tool);
		    
		    $Tool_used = $doc->createElement("Name");
        $Tool_used->appendTextNode($data_hash_ref->{$c_file}{'Toolname'});
			  $test_tool->appendChild($Tool_used);
			  
			  $Tool_version = $doc->createElement("Version");
        $Tool_version->appendTextNode($data_hash_ref->{$c_file}{'Version'});
			  $test_tool->appendChild($Tool_version);
			  
			  $test_verdict = $doc->createElement( "Verdict" );
			  $test_verdict->appendTextNode($data_hash_ref->{$c_file}{'Verdict'});
			  $test_result->appendChild($test_verdict);
			  
			  $testpart = $doc->createElement( "TestedPart" );
		    $test_result->appendChild($testpart);
		    
		    $UUT = $doc->createElement( "FileName" );
	      $UUT->appendTextNode($data_hash_ref->{$c_file}{'C_name'});
        $testpart->appendChild($UUT);
        
        $test_coverage = $doc->createElement( "Coverage" );
			  $testpart->appendChild($test_coverage);
			  
			  $test_metric_name = $doc->createElement( "MetricName" );
			  $test_metric_name->appendTextNode("C0");
			  $test_coverage->appendChild($test_metric_name);
			  
			  $test_value =$doc->createElement( "Value" ); 
			  $test_coverage->appendChild($test_value);
				
			  $test_percentage =$doc->createElement( "Percentage" ); 
        $test_percentage->appendTextNode($data_hash_ref->{$c_file}{'C0'});
			  $test_value->appendChild($test_percentage);
        
        $test_coverage = $doc->createElement( "Coverage" );
			  $testpart->appendChild($test_coverage);
			  
			  $test_metric_name = $doc->createElement( "MetricName" );
			  $test_metric_name->appendTextNode("C1");
			  $test_coverage->appendChild($test_metric_name);
			  
			  $test_value =$doc->createElement( "Value" ); 
			  $test_coverage->appendChild($test_value);
				
			  $test_percentage =$doc->createElement( "Percentage" ); 
        $test_percentage->appendTextNode($data_hash_ref->{$c_file}{'C1'});
			  $test_value->appendChild($test_percentage);	
			  

        $test_coverage = $doc->createElement( "Coverage" );
			  $testpart->appendChild($test_coverage);
			  
			  $test_metric_name = $doc->createElement( "MetricName" );
			  $test_metric_name->appendTextNode("MC/DC");
			  $test_coverage->appendChild($test_metric_name);
			  
			  $test_value =$doc->createElement( "Value" ); 
			  $test_coverage->appendChild($test_value);
				
			  $test_percentage =$doc->createElement( "Percentage" ); 
        $test_percentage->appendTextNode($data_hash_ref->{$c_file}{'MC/DC'});
			  $test_value->appendChild($test_percentage);
			  
			  $doc->setDocumentElement($root);
			  $data_hash_ref->{$c_file}{'C_name'} =~ s/\.c//ig;             
			  $doc->toFile($output_tpa."\\$data_hash_ref->{$c_file}{'C_name'}.tpa", 1);
			  
        print "\b";
    }
	
	
    print "\nTPA Files created successfully \n";
}

sub process_file {
    if (-f $_ && $_ =~ /\.c$/) {
        push @fileList, basename($_);
    } 
}
```

### File 6: RunPL.bat
## Instructions for Generation TAP Files
```bat
@echo off
del /s /q "%cd%\TPA_Files"
ECHO "Work Item Number wiil be considered in future updates - Now no work item number needed"
C:\tas\perl\v5_8_9\bin\perl.exe "%~dp0tpaFileGenerator.pl" "%~dp0Cantata\results\test_report.xml" "%cd%\TPA_Files" "Test_ChangeSet" " " " "
exit /b %ERRORLEVEL%

```
### Phase 0: Get User Input
**USER MUST PROVIDE the full path to the .c file FIRST**
- Example: `C:\Users\RGA8HC\Downloads\CHRYSLER_IPB\rb\as\ms\core\app\dcom\RBAPLCust\src\RBAPLCUST_Module.c`

### Phase 1: Create UT Folder Structure
1. **Extract filename** from provided path (without extension)
2. **Create UT folder** named `UT_<filename>` in parent directory of source file
3. **Create `src` subfolder** inside UT folder
4. **Copy source file** to `UT_<filename>\src\`
5. **Confirm structure created**

### Phase 2: Environment Selection
User selects AEEE environment via @aeee agent buttons (PRO or ECO).

### Phase 3: Auto-Detect AEEE Version
1. **Scan version directory**:
   - For AEEE-ECO: Scan `C:\toolbase\aeee_eco` 
   - For AEEE-PRO: Scan `C:\toolbase\aeee_pro`
2. **Find latest version**: Look for version folders (e.g., `2020.1.2`, `2023.1.0`)
3. **Use detected version**: Format as `call texec aeee_eco/VERSION` or `call texec aeee_pro/VERSION`

### Phase 4: Check Existing Files
1. **Check for existing files** in `UT_<filename>` folder
2. **Determine operation mode**:
   - If all 4 files exist → UPDATE mode (update `call texec` line only)
   - If some/none exist → CREATE mode

### Phase 5: Generate or Update Files
1. **For CREATE mode**:
   - Use the 4 templates above (File 1-4) exactly as shown
   - Create files in `UT_<filename>` folder
   - Replace ALL `call texec aeee_eco/2020.1.2` lines with detected version
   
2. **For UPDATE mode**:
   - Read existing files from `UT_<filename>` folder
   - Find and replace ONLY the `call texec` line with new detected version
   - Keep all other content unchanged

### Phase 6: Completion
Report to user:
- Source file provided: `<path_to_c_file>`
- UT folder created: `<parent_dir>\UT_<filename>`
- Source file copied to: `UT_<filename>\src\<filename>.c`
- Environment selected: AEEE-PRO or AEEE-ECO
- Version detected and used: e.g., `aeee_eco/2020.1.2`
- Files created/updated in `UT_<filename>` folder
- Ready to use with: `<bat_file> <PROJECT_PATH> <C_FILE_NAME>`
   - Replace paths with actual project paths
   - Update Cantata version (AEEE-PRO or AEEE-ECO)
   - Adjust compiler settings
   - Modify include directories
   - Update coverage rulesets
4. **Validate the generated files** by checking:
   - All paths are absolute or properly relative
   - Environment variables are correctly referenced
   - Error handling is in place
   - Correct AEEE environment is referenced

## Example Usage
After batch files are created, they can be used like:
```cmd
REM Step 1: Compile the source file
<PROJECT_PATH> \compile_project.bat "C:\Projects\MyProject\Cantata" "module"

REM Step 2: Generate test scripts
<PROJECT_PATH>\generate_test.bat "C:\Projects\MyProject\Cantata"

REM Step 3: Build and run tests
<PROJECT_PATH>\build_test.bat "C:\Projects\MyProject" "module"

REM Step 4: Generate test report
<PROJECT_PATH> \generate_test_summary.bat "C:\Projects\MyProject\Cantata"
```

## Environment-Specific Examples

### AEEE-PRO Environment
```bat
REM In the batch files, use:
call texec aeee_pro/2023.1.0
```

### AEEE-ECO Environment
```bat
REM In the batch files, use:
call texec aeee_eco/2020.1.2
```

## Notes
- **STEP 0**: User MUST provide full path to .c file before any processing
- **Folder Structure**: Automatically create `UT_<filename>` folder with `src` subfolder
- **Source Copy**: Copy provided .c file to `UT_<filename>\src\` folder
- All batch files assume Windows environment with PowerShell/CMD
- Cantata environment must be properly installed and configured
- The `texec` command must be available in the system PATH
- Environment variables like `%UBK_PRODUCT%` and `%TB_ECL_CANTATA_HOME%` must be set by Cantata installation
- Test directory structure follows Cantata conventions: `<PROJECT_PATH>\Cantata\tests\atest_<C_FILE>\`
- **Version Selection**: After scanning available versions, ASK user which version to use - DO NOT automatically select latest version
- **User Confirmation Required**: Wait for user to confirm version selection before creating/updating batch files
- **Templates Embedded**: All 4 batch file templates are included in this prompt (File 1-4 above) - no external files needed
- **C File Name**: Not needed during creation - passed as parameter `%2` when running the batch file
- **Single Change**: Only update the `call texec` line with user-selected version - keep everything else from templates exactly as shown