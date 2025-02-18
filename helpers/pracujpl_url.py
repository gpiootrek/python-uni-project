categories_map = {
    'data': 'big-data-science'
}
experience_map = {
    'trainee': '1',
    'junior': '17',
    'mid': '4',
    'senior': '18',
    'expert': '19'
}
skills_map = {
    'javascript': '33',
    'html': '34',
    'sql': '36',
    'python': '37',
    'java': '38'
}

def create_url(category: str = '', exp: str = '', skill: str = '') -> str:
    url = 'https://it.pracuj.pl/praca?'
    params = []
    
    if len(category) > 0:
        if category in categories_map:
            params.append(f'its={categories_map[category]}')
        else:
            params.append(f'its={category.lower()}')
    if len(exp) > 0:
        params.append(f'et={experience_map[exp.lower()]}')
    if len(skill) > 0:
        params.append(f'iith={skills_map[skill.lower()]}')
    
    params = '&'.join(params)
    
    return f'{url}{params}'
