def create_url(categories: str, requirements: str, exp: str) -> str:
    url = 'https://nofluffjobs.com/pl/'
    
    if len(categories) > 0:
        url += f'{categories}?criteria='
    if len(exp) > 0:
        url += f'exp%3D{exp}%20'
    if len(requirements) > 0:
        url += f'requirement%3D{requirements}'
    
    return url
