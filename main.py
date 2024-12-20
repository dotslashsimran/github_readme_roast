import openai
import requests
import base64
import agentops
from typing import Dict, Any

class ReadmeAnalyzer:
    def __init__(self):
        """Initialize the ReadmeAnalyzer with API credentials."""
        openai_api_key = "****************************"
        agentops_api_key = "*****************"
        agentops.init(agentops_api_key)
        openai.api_key = openai_api_key
        
    def get_readme_content(self, owner: str, repo: str) -> str:
        """Fetch README content from a GitHub repository."""
        url = f'https://api.github.com/repos/{owner}/{repo}/readme'
        response = requests.get(url)
        
        if response.status_code == 200:
            return base64.b64decode(response.json()['content']).decode('utf-8')
        else:
            raise Exception(f"Failed to fetch README: {response.status_code}")

    def roast_readme(self, readme_content: str) -> Dict[Any, Any]:
        """Analyze README content and provide a humorous roast."""
        prompt = f"""You're a MEAN but in a funny way - code reviewer who's tired of reading bad README files. 
        Analyze this README and:
        1. Give it a brutal score out of 10
        2. Roast it mercilessly (be funny and a little mean)
        3. Point out what's missing or could be better
        4. Add at least one sarcastic comment about the writing style
        
        Make it entertaining but keep it conversational (the writing tone).
        
        README content:
        {readme_content}
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a witty and sarcastic code reviewer who specializes in roasting README files."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        feedback = {
            'roast': response.choices[0].message.content,
            'score': self._calculate_score(response.choices[0].message.content)
        }
        
        return feedback
    
    def _calculate_score(self, analysis: str) -> float:
        """Calculate a score based on the roast content."""
        brutal_indicators = [
            'missing', 'unclear', 'lacks', 'incomplete',
            'what even is this', 'seriously', 'facepalm',
            'why', 'confused', 'help'
        ]
        
        score = 8.0  # Start optimistic
        
        for word in brutal_indicators:
            if word in analysis.lower():
                score -= 0.5
                
        return min(max(score, 0), 10)  # Keep it between 0 and 10

def main():
    analyzer = ReadmeAnalyzer()
    
    owner = input("Enter GitHub repository owner: ")
    repo = input("Enter repository name: ")
    
    try:
        print(f"\n🔍 Analyzing {owner}/{repo}'s README...\n")
        readme_content = analyzer.get_readme_content(owner, repo)
        roast = analyzer.roast_readme(readme_content)
        
        print("🔥 ROAST RESULTS 🔥")
        print("=" * 50)
        print(roast['roast'])
        print("\n" + "=" * 50)
        print(f"Final Score: {roast['score']}/10 ")
        
    except Exception as e:
        print(f"💀 Error: {str(e)}")

if __name__ == "__main__":
    main()