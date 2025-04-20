import asyncio
import httpx
import logging
from typing import Dict, Any, Optional

from app.config import settings
from app.utils.exceptions import AIModelException

logger = logging.getLogger(__name__)

class LlamaInterface:
    """Interface for interacting with the LLaMA3 model"""
    
    def __init__(self):
        self.model_host = settings.LLAMA_MODEL_HOST
        self.model_port = settings.LLAMA_MODEL_PORT
        self.base_url = f"http://{self.model_host}:{self.model_port}"
        self.client = httpx.AsyncClient(timeout=60.0)  # Longer timeout for AI operations
    
    async def generate_summary(self, content: str, max_tokens: int = 300) -> str:
        """
        Generate a summary of the provided content using LLaMA3
        
        Args:
            content: Text content to summarize
            max_tokens: Maximum number of tokens in the summary
            
        Returns:
            Generated summary text
        """
        try:
            prompt = self._create_summary_prompt(content)
            response = await self._generate_text(prompt, max_tokens)
            return self._extract_summary(response)
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            raise AIModelException(f"Failed to generate summary: {str(e)}")
    
    async def generate_recommendations(self, user_preferences: Dict[str, Any], books_read: list) -> list:
        """
        Generate book recommendations based on user preferences and reading history
        
        Args:
            user_preferences: Dictionary of user preferences
            books_read: List of books the user has already read
            
        Returns:
            List of recommended books with explanations
        """
        try:
            prompt = self._create_recommendation_prompt(user_preferences, books_read)
            response = await self._generate_text(prompt, max_tokens=500)
            return self._extract_recommendations(response)
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            raise AIModelException(f"Failed to generate recommendations: {str(e)}")
    
    async def _generate_text(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str:
        """
        Send request to LLaMA3 model to generate text
        
        Args:
            prompt: Text prompt for the model
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (higher = more creative)
            
        Returns:
            Generated text from the model
        """
        payload = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        
        try:
            # For local LLaMA3 model, adjust endpoint as needed
            response = await self.client.post(f"{self.base_url}/generate", json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("text", "")
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during AI request: {e.response.status_code} - {e.response.text}")
            raise AIModelException(f"HTTP error: {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"Error communicating with AI service: {e}")
            raise AIModelException(f"Connection error: {str(e)}")
    
    def _create_summary_prompt(self, content: str) -> str:
        """Create a prompt for book summary generation"""
        return f"""Please provide a concise summary of the following book content in 3-5 paragraphs. 
Focus on the main themes, characters, and plot elements.

BOOK CONTENT:
{content}

SUMMARY:"""
    
    def _create_recommendation_prompt(self, preferences: Dict[str, Any], books_read: list) -> str:
        """Create a prompt for book recommendation generation"""
        books_read_str = "\n".join([f"- {book['title']} by {book['author']}" for book in books_read])
        genres = ", ".join(preferences.get("preferred_genres", []))
        
        return f"""Please recommend 5 books based on the following user preferences and reading history.
For each recommendation, explain why it fits the user's taste in 2-3 sentences.

USER PREFERENCES:
- Preferred genres: {genres}
- Favorite authors: {', '.join(preferences.get('favorite_authors', []))}
- Interests: {', '.join(preferences.get('interests', []))}

BOOKS ALREADY READ:
{books_read_str}

RECOMMENDATIONS:"""
    
    def _extract_summary(self, response: str) -> str:
        """Extract and clean up the generated summary"""
        # Simple extraction, may need refinement based on actual model output format
        if not response:
            return "Could not generate summary."
        
        # Remove any prefixes like "SUMMARY:" if present
        if "SUMMARY:" in response:
            response = response.split("SUMMARY:", 1)[1]
        
        return response.strip()
    
    def _extract_recommendations(self, response: str) -> list:
        """Extract and structure the book recommendations"""
        if not response:
            return []
        
        recommendations = []
        # Simple parsing - in real implementation, would use more robust parsing
        lines = response.strip().split("\n")
        current_rec = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith("- ") or line.startswith("1. ") or any(str(i)+"." in line[:3] for i in range(1, 6)):
                # New recommendation
                if current_rec and "title" in current_rec:
                    recommendations.append(current_rec)
                current_rec = {}
                
                # Extract title and author
                parts = line.split(" by ", 1)
                if len(parts) == 2:
                    title = parts[0].lstrip("- 123456789. ")
                    current_rec["title"] = title
                    current_rec["author"] = parts[1].split(":", 1)[0].strip()
                    
                    # Extract explanation if on same line
                    if ":" in parts[1]:
                        current_rec["explanation"] = parts[1].split(":", 1)[1].strip()
            elif current_rec and "title" in current_rec and "explanation" not in current_rec:
                # This line is likely the explanation
                current_rec["explanation"] = line
                
        # Add the last recommendation
        if current_rec and "title" in current_rec:
            recommendations.append(current_rec)
            
        return recommendations