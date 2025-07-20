#!/usr/bin/env python3
"""
Evaluation Test Script for Data Analyst Agent
Simulates the 20-point rubric evaluation
"""

import requests
import json
import re
import math
import base64
import time
from typing import List, Any

class DataAnalystEvaluator:
    def __init__(self, api_url: str = "http://localhost:8000/api/"):
        self.api_url = api_url
        self.total_score = 0
        self.max_score = 20
        
    def test_api_response(self, question_file: str = "question.txt") -> List[Any]:
        """Test the API with the question file and return the response"""
        print(f"🔄 Testing API endpoint: {self.api_url}")
        
        try:
            with open(question_file, 'rb') as f:
                files = {'file': f}
                start_time = time.time()
                response = requests.post(self.api_url, files=files, timeout=180)
                end_time = time.time()
            
            print(f"⏱️  Response time: {end_time - start_time:.2f} seconds")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ API response received successfully")
                print(f"📄 Response type: {type(result)}")
                print(f"📊 Response preview: {str(result)[:200]}...")
                return result
            else:
                print(f"❌ API error: {response.status_code}")
                print(f"Error details: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
            return None
    
    def evaluate_structure(self, result: List[Any]) -> bool:
        """Test 1: Structural gate - must be 4-element array"""
        print("\n🔍 Test 1: Structural Validation")
        
        if not isinstance(result, list):
            print("❌ Response is not an array")
            return False
            
        if len(result) != 4:
            print(f"❌ Array has {len(result)} elements, expected 4")
            return False
            
        print("✅ Response is a 4-element array")
        return True
    
    def evaluate_first_answer(self, result: List[Any]) -> bool:
        """Test 2: First answer must equal 1 (4 points)"""
        print("\n🔍 Test 2: First Answer (4 points)")
        
        try:
            first_answer = result[0]
            if first_answer == 1:
                print(f"✅ First answer is correct: {first_answer}")
                self.total_score += 4
                return True
            else:
                print(f"❌ First answer is incorrect: {first_answer} (expected: 1)")
                return False
        except Exception as e:
            print(f"❌ Error evaluating first answer: {e}")
            return False
    
    def evaluate_second_answer(self, result: List[Any]) -> bool:
        """Test 3: Second answer must contain "Titanic" (4 points)"""
        print("\n🔍 Test 3: Second Answer (4 points)")
        
        try:
            second_answer = str(result[1])
            if re.search(r'titanic', second_answer, re.I):
                print(f"✅ Second answer contains 'Titanic': {second_answer}")
                self.total_score += 4
                return True
            else:
                print(f"❌ Second answer doesn't contain 'Titanic': {second_answer}")
                return False
        except Exception as e:
            print(f"❌ Error evaluating second answer: {e}")
            return False
    
    def evaluate_third_answer(self, result: List[Any]) -> bool:
        """Test 4: Third answer within ±0.001 of 0.485782 (4 points)"""
        print("\n🔍 Test 4: Third Answer (4 points)")
        
        try:
            third_answer = float(result[2])
            expected = 0.485782
            tolerance = 0.001
            
            if abs(third_answer - expected) <= tolerance:
                print(f"✅ Third answer is within tolerance: {third_answer} (expected: {expected})")
                self.total_score += 4
                return True
            else:
                difference = abs(third_answer - expected)
                print(f"❌ Third answer outside tolerance: {third_answer} (diff: {difference}, max: {tolerance})")
                return False
        except Exception as e:
            print(f"❌ Error evaluating third answer: {e}")
            return False
    
    def evaluate_plot(self, result: List[Any]) -> bool:
        """Test 5: Plot validation (8 points)"""
        print("\n🔍 Test 5: Plot Validation (8 points)")
        
        try:
            plot_data = result[3]
            
            # Check if it's a valid data URI
            is_data_uri = plot_data.startswith('data:image/')
            print(f"📊 Valid data URI: {is_data_uri}")
            
            # Check if it contains base64 data
            has_base64 = 'base64,' in plot_data
            print(f"🔢 Contains base64: {has_base64}")
            
            # Check size (rough estimate)
            size_bytes = len(plot_data.encode('utf-8'))
            size_ok = size_bytes < 100000
            print(f"📏 Size check: {size_bytes} bytes (<100KB: {size_ok})")
            
            # Try to decode base64 (basic validation)
            try:
                if 'base64,' in plot_data:
                    base64_part = plot_data.split('base64,')[1]
                    decoded = base64.b64decode(base64_part)
                    can_decode = True
                    print(f"🔓 Base64 decodes successfully: {len(decoded)} bytes")
                else:
                    can_decode = False
                    print("❌ No base64 data found")
            except Exception as decode_error:
                can_decode = False
                print(f"❌ Base64 decode failed: {decode_error}")
            
            # Award points based on criteria
            criteria_met = [is_data_uri, has_base64, size_ok, can_decode]
            points_per_criterion = 2  # 8 points / 4 criteria
            points_earned = sum(criteria_met) * points_per_criterion
            
            self.total_score += points_earned
            
            if all(criteria_met):
                print(f"✅ Plot validation passed: {points_earned}/8 points")
                return True
            else:
                print(f"⚠️  Plot validation partial: {points_earned}/8 points")
                return False
                
        except Exception as e:
            print(f"❌ Error evaluating plot: {e}")
            return False
    
    def run_evaluation(self, question_file: str = "question.txt") -> dict:
        """Run the complete evaluation and return results"""
        print("🚀 Starting Data Analyst Agent Evaluation")
        print("=" * 50)
        
        # Test API response
        result = self.test_api_response(question_file)
        if result is None:
            return {
                "success": False,
                "score": 0,
                "max_score": self.max_score,
                "percentage": 0,
                "details": "API request failed"
            }
        
        # Run all tests
        tests = [
            ("Structure", self.evaluate_structure, 0),
            ("First Answer", self.evaluate_first_answer, 4),
            ("Second Answer", self.evaluate_second_answer, 4), 
            ("Third Answer", self.evaluate_third_answer, 4),
            ("Plot Validation", self.evaluate_plot, 8)
        ]
        
        structure_passed = self.evaluate_structure(result)
        if not structure_passed:
            return {
                "success": False,
                "score": 0,
                "max_score": self.max_score,
                "percentage": 0,
                "details": "Failed structural validation - not a 4-element array"
            }
        
        # Run content tests
        self.evaluate_first_answer(result)
        self.evaluate_second_answer(result)
        self.evaluate_third_answer(result)
        self.evaluate_plot(result)
        
        # Calculate final score
        percentage = (self.total_score / self.max_score) * 100
        
        print("\n" + "=" * 50)
        print(f"🏆 EVALUATION COMPLETE")
        print(f"📊 Final Score: {self.total_score}/{self.max_score} ({percentage:.1f}%)")
        
        if percentage >= 90:
            print("🌟 EXCELLENT! Your agent should pass the evaluation!")
        elif percentage >= 70:
            print("✅ GOOD! Your agent has a strong chance of success!")
        elif percentage >= 50:
            print("⚠️  FAIR! Some improvements needed for optimal performance!")
        else:
            print("❌ NEEDS WORK! Significant improvements required!")
        
        return {
            "success": True,
            "score": self.total_score,
            "max_score": self.max_score,
            "percentage": percentage,
            "details": f"Evaluation completed successfully",
            "response": result
        }

def main():
    """Main evaluation function"""
    evaluator = DataAnalystEvaluator()
    results = evaluator.run_evaluation()
    
    # Save results
    with open("evaluation_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to evaluation_results.json")
    return results

if __name__ == "__main__":
    main()
