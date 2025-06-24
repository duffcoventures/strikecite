import requests
import json
import sys
from datetime import datetime

class StrikeCiteAPITester:
    def __init__(self, base_url="https://15d824e4-b2a9-4f5c-b57b-6fd60de96aa7.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                return success, response.json()
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                return False, response.text

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, str(e)

    def test_health_endpoint(self):
        """Test the health check endpoint"""
        print("\n=== Testing Health Endpoint ===")
        success, response = self.run_test(
            "Health Check",
            "GET",
            "health",
            200
        )
        if success:
            print(f"Health Status: {response['status']}")
            print(f"Reporters Loaded: {response['reporters_loaded']}")
            if response['reporters_loaded'] != 32:
                print(f"⚠️ Warning: Expected 32 reporters, got {response['reporters_loaded']}")
            else:
                print(f"✅ Correct number of reporters loaded: 32")
        return success

    def test_reporters_endpoint(self):
        """Test the reporters endpoint"""
        print("\n=== Testing Reporters Endpoint ===")
        success, response = self.run_test(
            "Get Reporters",
            "GET",
            "reporters",
            200
        )
        if success:
            print(f"Received {len(response)} reporters")
            if len(response) != 32:
                print(f"⚠️ Warning: Expected 32 reporters, got {len(response)}")
            else:
                print(f"✅ Correct number of reporters loaded: 32")
            
            # Check for different types of reporters
            federal_reporters = [r for r in response if r.get('jurisdiction') == 'Federal']
            regional_reporters = [r for r in response if r.get('jurisdiction') == 'Regional']
            
            print(f"Federal reporters: {len(federal_reporters)}")
            print(f"Regional reporters: {len(regional_reporters)}")
            
            # Check specific reporters
            reporters_to_check = ['U.S.', 'F.3d', 'So. 2d', 'N.E.', 'P.3d']
            for abbr in reporters_to_check:
                reporters_found = [r for r in response if r.get('abbreviation') == abbr]
                if reporters_found:
                    print(f"✅ Found {abbr} reporter")
                else:
                    print(f"❌ Missing {abbr} reporter")
                
        return success

    def test_validate_citations_endpoint(self):
        """Test the validate-citations endpoint (Layer A)"""
        print("\n=== Testing Validate Citations Endpoint (Layer A) ===")
        
        # Sample LOOKUP_JSON as specified in the requirements
        lookup_json = [
            {
                "citation": "410 U.S. 113", 
                "normalized_citations": ["410 U.S. 113"], 
                "start_index": 22, 
                "end_index": 32, 
                "status": 200, 
                "clusters": [{"url": "https://example.com"}]
            },
            {
                "citation": "123 F3rd 456", 
                "normalized_citations": [], 
                "start_index": 50, 
                "end_index": 61, 
                "status": 404, 
                "clusters": []
            },
            {
                "citation": "999 So. 2d 123", 
                "normalized_citations": ["999 So. 2d 123"], 
                "start_index": 80, 
                "end_index": 94, 
                "status": 200, 
                "clusters": [{"url": "https://example.com"}]
            }
        ]
        
        success, response = self.run_test(
            "Validate Citations",
            "POST",
            "validate-citations",
            200,
            data=lookup_json
        )
        
        if success:
            print("Citation validation response received")
            if 'citations' in response and 'summary' in response:
                print(f"✅ Response contains citations and summary")
                
                # Check if we have the right number of citations
                if len(response['citations']) == 3:
                    print(f"✅ All 3 citations were processed")
                else:
                    print(f"❌ Expected 3 citations, got {len(response['citations'])}")
                
                # Check individual citations
                for i, citation in enumerate(response['citations']):
                    print(f"\nCitation {i+1}: {citation['raw']}")
                    print(f"  Normalized: {citation['normalized']}")
                    print(f"  Verified: {citation['verified']}")
                    print(f"  Reporter: {citation['reporter']}")
                    
                    # Check for typo detection in the F3rd citation
                    if citation['raw'] == "123 F3rd 456":
                        if "typo" in citation['note'].lower() and "F.3d" in citation['note']:
                            print(f"✅ Correctly identified typo in 'F3rd' and suggested 'F.3d'")
                        else:
                            print(f"❌ Failed to detect typo in 'F3rd' or suggest 'F.3d'")
                            print(f"  Note: {citation['note']}")
                
                # Check summary
                print(f"\nSummary: Total: {response['summary']['total']}, Verified: {response['summary']['verified']}, Confidence: {response['summary']['confidence']}")
            else:
                print("❌ Response missing expected fields")
                
        return success

    def test_validate_text_endpoint(self):
        """Test the validate-text endpoint (Layer B)"""
        print("\n=== Testing Validate Text Endpoint (Layer B) ===")
        
        # Sample text as specified in the requirements
        text_data = {
            "text": "Roe v. Wade, 410 U.S. 113 (1973), and Smith v. Jones, 123 F3rd 456 (invalid citation)."
        }
        
        success, response = self.run_test(
            "Validate Text",
            "POST",
            "validate-text",
            200,
            data=text_data
        )
        
        if success:
            print("Text validation response received")
            if 'citations' in response and 'summary' in response:
                print(f"✅ Response contains citations and summary")
                
                # Check if any citations were found
                if len(response['citations']) > 0:
                    print(f"✅ Found {len(response['citations'])} citations")
                    
                    # Check for specific citations
                    roe_citations = [c for c in response['citations'] if "410 U.S. 113" in c['normalized']]
                    if roe_citations and roe_citations[0]['verified']:
                        print(f"✅ Roe v. Wade citation was verified")
                    else:
                        print(f"❌ Roe v. Wade citation was not verified or not found")
                    
                    # Check for typo detection in the F3rd citation
                    f3rd_citations = [c for c in response['citations'] if "F3rd" in c['raw']]
                    if f3rd_citations:
                        if "typo" in f3rd_citations[0]['note'].lower() and "F.3d" in f3rd_citations[0]['note']:
                            print(f"✅ Correctly identified typo in 'F3rd' and suggested 'F.3d'")
                        else:
                            print(f"❌ Failed to detect typo in 'F3rd' or suggest 'F.3d'")
                            print(f"  Note: {f3rd_citations[0]['note']}")
                    else:
                        print(f"❌ Failed to find the F3rd citation")
                else:
                    print(f"❌ No citations found in the text")
                
                # Check confidence scoring
                print(f"Confidence: {response['summary']['confidence']}")
                print(f"Summary: Total: {response['summary']['total']}, Verified: {response['summary']['verified']}, Unverified: {response['summary']['unverified']}")
            else:
                print("❌ Response missing expected fields")
                
        return success

def main():
    # Setup
    tester = StrikeCiteAPITester()
    
    # Run tests
    health_success = tester.test_health_endpoint()
    reporters_success = tester.test_reporters_endpoint()
    validate_citations_success = tester.test_validate_citations_endpoint()
    validate_text_success = tester.test_validate_text_endpoint()
    
    # Print results
    print(f"\n📊 Tests passed: {tester.tests_passed}/{tester.tests_run}")
    
    # Return success status
    return 0 if (health_success and reporters_success and 
                validate_citations_success and validate_text_success) else 1

if __name__ == "__main__":
    sys.exit(main())