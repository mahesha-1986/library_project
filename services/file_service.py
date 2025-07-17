import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def Read_DepartmentCodes():
        """Load department codes from file or use default mapping"""
        try:
            departments = {}
            with open('department_codes.txt', 'r', encoding='utf-8') as file:
                for line in file:
                    if line.strip():
                        code, name = line.strip().split(' - ')
                        departments[name.lower()] = code
            return departments
        except Exception as e:
            logger.error(f"Error loading department codes: {str(e)}")
            return {
                "chemistry": "BBHCCHE",
                "commerce": "BBHCCOM",
                "competitive exam": "BBHCCOMP",
                "computer science": "BBHCCSC",
                "dictionary": "BBHCDIC",
                "economics": "BBHCECO",
                "encyclopedia": "BBHCENC",
                "english": "BBHCENG",
                "general science": "BBHCGEN",
                "hindi": "BBHCHIN",
                "kannada": "BBHCKAN",
                "management": "BBHCMAN",
                "mathematics": "BBHCMAT",
                "physical education": "BBHCPHY",
                "physics": "BBHCPHYS",
                "political science": "BBHCPOL",
                "research methodology": "BBHCRES",
                "sanskrit": "BBHCSAN",
                "year book": "BBHCYEA"
            }