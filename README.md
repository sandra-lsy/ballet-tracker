# Ballet Tracker
#### Video Demo: <URL HERE>
#### Description:

Ballet Tracker is a web application that helps ballet enthusiasts discover and organise classical ballet videos. Built with Flask and integrated with the YouTube API, it provides an intelligent search system for finding specific ballet variations, acts and scenes.

## Project Overview

This application serves as a comprehensive ballet video discovery platform. Users can browse through a curated collection of famous ballets, search for specific performances using search queries, and bookmark their favorite videos with personal notes.

## Files and Functionality

### Core Application Files

**app.py** - The main Flask application containing all route handlers and core functionality. This file manages the web server, handles user requests, and coordinates between different components. It includes routes for the home page, ballet details, custom searches, and bookmark management.

**ballet_search.py** - Contains the `BalletSearchEngine` class that generates intelligent search queries for YouTube. This engine understands ballet terminology and can build specific searches based on characters, acts, scene types, and ballet-specific vocabulary. It includes methods for suggesting common searches and building custom queries.

**youtube_api.py** - Handles all YouTube API interactions through the `YouTubeAPI` class. It searches for videos, processes results, and includes fallback functionality when the API is unavailable. The class handles errors and formats video data for the frontend.

### Data Files

**data/ballets.json** - Contains structured information about major ballets including titles, composers, main characters, number of acts, and brief descriptions. This serves as the knowledge base for the search engine.

**data/bookmarks.json** - Stores user bookmarks with video information and personal notes. This file is created and updated dynamically as users bookmark videos.

### Templates

**templates/base.html** - The base template that provides consistent styling and navigation across all pages. Uses Bootstrap for responsive design.

**templates/index.html** - The home page displaying a grid of available ballets with cover images and basic information.

**templates/ballet_details.html** - The detailed view for each ballet, showing video search results, custom search options, and bookmark functionality. This is the most complex template with JavaScript for dynamic interactions.

**templates/bookmarks.html** - Displays all saved bookmarks with options to remove them and re-watch videos.

**templates/error.html** - Simple error page for handling error conditions.

## Design Decisions

### Search Engine Architecture
I chose to build a custom search engine rather than using simple keyword matching because classical ballet has specific terminology and structure. The engine understands concepts like "pas de deux," "variation," and "Act I" and can generate more targeted YouTube searches.

### JSON Data Storage
For this project scope, I used JSON files for data persistence rather than a full database. This keeps the project simple while still demonstrating data management concepts. The ballet data is relatively static, and bookmarks don't require complex relationships.

### API Integration with Fallbacks
The YouTube API integration includes comprehensive error handling and demo video fallbacks. This ensures the application remains functional even when API keys are missing or quota limits are reached, making it more robust for demonstration purposes.

### Modular Code Structure
I created different modules (app.py for routes, ballet_search.py for search logic, youtube_api.py for API handling) to make the code more maintainable and easier to understand.

### Bootstrap Frontend
I chose Bootstrap for the frontend to create a responsive interface without spending excessive time on custom CSS. This allowed me to focus on the backend functionality while still delivering a polished user experience.

## Technical Challenges

The most significant challenge was creating search queries that would return relevant ballet videos from YouTube's vast library. I solved this by building a terminology-aware search engine that understands ballet structure and can combine multiple search terms effectively.

Another challenge was handling API reliability and quota limits. I implemented a fallback system that shows a demo video when the API is unavailable, ensuring the application always functions for demonstration purposes.

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Create `.env` file with your YouTube API key
6. Run: `python app.py`

## Future Enhancements

Potential improvements could include user authentication, more sophisticated video filtering, bookmark notes editing, and a more comprehensive ballet database with historical performance information.