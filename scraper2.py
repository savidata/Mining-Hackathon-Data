import requests
from bs4 import BeautifulSoup
import csv
import sys
import asyncio

#-------------------------------------------
#   Data Checklist
#-------------------------------------------
# [x] project title
# [x] Number of slides
# [x] # of words in description
# [x] List of ‘built w/‘ tags
# [x] # of team members
# [x] avg. win ratio of team members
# [x] Avg. submit ratio of team members
# [x] List of unique skills for all team members
# [x] Avg # of interests
# [x] Avg # of Hackathons registered to
# [x] Avg # of followers
# [x] Avg # of following
# [x] Avg # of likes

#-------------------------------------------
#   Data From Team Member Cheecklist
#-------------------------------------------
# [x] list of skills
# [x] list of interest
# [x] # of projcts
# [x] # of winning projcts
# [x] # of hackathons
# [x] # of followers
# [x] # of following
# [x] # of likes

#-------------------------------------------
#   Utils
#-------------------------------------------
def getCSVFromList(list): 
    return ','.join(list)

def getAvg(a, b): 
    return 0 if b == 0 else a/b

#-------------------------------------------
#   Get Team Member Data
#-------------------------------------------
async def getTeamMemberData(teamMemberUrl): 

    print('MEMBER: ' + teamMemberUrl)

    # Get data from page
    response = requests.get(teamMemberUrl)
    content = response.content
    memberPageSoup = BeautifulSoup(content, 'html.parser')

    # Get list of skills
    skills = []
    portfolioTags = memberPageSoup.find('ul', {'class': 'portfolio-tags'})
    if portfolioTags != None: 
        skillSpans = portfolioTags.find_all('span', {'class': 'cp-tag'})
        if skillSpans != None: 
            for span in skillSpans: 
                skill = span.text.strip()
                skills.append(skill)

    # Get list of interest
    interests = []
    interestSpans = memberPageSoup.find_all('span', {'class': 'cp-tag theme'})
    if interestSpans != None: 
        for span in interestSpans: 
            interest = span.text.strip()
            interests.append(interest)

    # Get # of projects
    projectCount = 0
    winningProjectCount = 0
    projectContainers = memberPageSoup.find_all('div', {'class': 'gallery-item'})
    if projectContainers != None: 
        for project in projectContainers: 
            isWinner = (project.find('img', {'class': 'winner'}) != None)
            projectCount = projectCount + 1
            if isWinner: 
                winningProjectCount = winningProjectCount + 1

    # Get # of hackathons
    hackathonCount = 0
    followersCount = 0
    followingCount = 0
    likeCount = 0
    portfolioNavigation = memberPageSoup.find('nav', {'id': 'portfolio-navigation'})
    if portfolioNavigation != None: 
        links = portfolioNavigation.find_all('a')
        for link in links: 
            linkTitle = link.text.strip()
            elements = linkTitle.split()

            if elements[1] == 'Hackathons': 
                hackathonCount = int(elements[0])
            if elements[1] == 'Followers': 
                followersCount = int(elements[0])
            if elements[1] == 'Following': 
                followingCount = int(elements[0])
            if elements[1] == 'Likes': 
                likeCount = int(elements[0])

    teamMember = {
        'skills': skills, 
        'interests': interests, 
        'projectCount': projectCount, 
        'winningCount': winningProjectCount, 
        'hackathonCount': hackathonCount,
        'followerCount': followersCount, 
        'followingCount': followingCount, 
        'likeCount': likeCount
    }

    return teamMember


#-------------------------------------------
#   Get Proejct Data
#-------------------------------------------
async def getProjectData(projectUrl, hackathonUrl): 

    print('PROEJCT: ' + projectUrl)

    # Get data from page
    response = requests.get(projectUrl)
    content = response.content
    projectPageSoup = BeautifulSoup(content, 'html.parser')

    # Find project title
    title = projectPageSoup.find('h1').text

    # Find number of images
    imageCount = 0
    foundImages = projectPageSoup.find_all('img', {'class': 'software_photo_image'})
    if foundImages != None: 
        imageCount = len(foundImages)
        
    
    # Get total word count from paragraphs in body (currently excludes titles)
    app_details = projectPageSoup.find('div', {'id': 'app-details-left'})
    descriptionWordCount = 0
    if app_details != None: 
        paragraphs = app_details.find_all('p')
        total = 0
        for paragraph in paragraphs: 
            words = paragraph.text.split()
            total += len(words)
        descriptionWordCount = total

    # Get list of built with tags
    builtWithContainer = projectPageSoup.find('div', {'id': 'built-with'})
    builtWithTags = []
    if builtWithContainer != None: 
        builtWithLinks = builtWithContainer.find_all('a')
        for tag in builtWithLinks: 
            builtWithTags.append(tag.text)

    # Get number of team members
    appTeam = projectPageSoup.find_all('li', {'class': 'software-team-member'})
    teamMembers = []
    if appTeam != None: 
        for member in appTeam: 
            teamMemberLinks = member.find_all('a', {'class': 'user-profile-link'})
            if teamMemberLinks != None and len(teamMemberLinks) != 0: 
                memberUrl = teamMemberLinks[0]['href']
                teamMemberData = await getTeamMemberData(memberUrl)
                teamMembers.append(teamMemberData)

    # Determine if the project won anything
    wins = 0
    didWin = 0
    winnerSpans = projectPageSoup.find_all('span', {'class': 'winner'})
    if winnerSpans != None: 
        didWin = 1 if (len(winnerSpans) > 0) else 0 
        wins = len(winnerSpans)

    # Calculate information that is based on collective team member stats
    numberOfTeamMembers = len(teamMembers)

    totalProjects = 0
    totalWins = 0
    totalHackathons = 0
    totalFollowing = 0
    totalFollowers = 0
    totalLikes = 0
    totalInterest = 0
    uniqueSkills = set()
    totalSkills = []
    uniqueSkillCount = 0
    totalSkillCount = 0
    totalSubmitToRegistered = 0

    for member in teamMembers: 
        totalProjects += member['projectCount']
        totalWins += member['winningCount']
        totalHackathons += member['hackathonCount']
        totalFollowing += member['followerCount']
        totalFollowers += member['followingCount']
        totalLikes += member['likeCount']
        totalInterest += len(member['interests'])
        skills = member['skills']

        totalSubmitToRegistered += getAvg(member['projectCount'], member['hackathonCount'])

        for skill in skills: 
            uniqueSkills.add(skill)
            totalSkills.append(skill)
    
    uniqueSkillCount = len(uniqueSkills)
    totalSkillCount = len(totalSkills)

    
    project = {
        'title': title,
        'hackathon_url': hackathonUrl,
        'did_win': didWin, 
        'p_win_count': wins,
        'number_of_slides': imageCount,
        'description_word_count': descriptionWordCount, 
        'built_with_tags': getCSVFromList(builtWithTags), 
        'built_with_count': len(builtWithTags),
        'team_member_count': numberOfTeamMembers, 
        'total_wins': totalWins,
        'total_projects': totalProjects,
        'submit_to_registered': getAvg(totalSubmitToRegistered, numberOfTeamMembers),
        'unique_skills': getCSVFromList(uniqueSkills), 
        'u_skill_count': uniqueSkillCount, 
        'avg_num_skills': getAvg(totalSkillCount, numberOfTeamMembers), 
        'avg_interest': getAvg(totalInterest, numberOfTeamMembers),
        'avg_hackathons': getAvg(totalHackathons, numberOfTeamMembers), 
        'avg_followers': getAvg(totalFollowers, numberOfTeamMembers), 
        'avg_following': getAvg(totalFollowing, numberOfTeamMembers),
        'avg_likes': getAvg(totalLikes, numberOfTeamMembers)
    }

    return project

#-------------------------------------------
#   Get Submission Page Data
#-------------------------------------------
async def getProjectsFromPage(baseUrl, endpoint): 

    url = baseUrl + endpoint

    # Get data from page
    response = requests.get(url)
    content = response.content
    pageSoup = BeautifulSoup(content, 'html.parser')

    # Look for all projects on the page
    projects = pageSoup.findAll('div', {'class': 'gallery-item'})

    projectsList = []
    for project in projects: 

        # Get the url for the project page
        projectLink = project.find('a', {'class': 'link-to-software'})

        if projectLink != None: 
            projectUrl = projectLink['href']
            projectData = await getProjectData(projectUrl, baseUrl)
            projectsList.append(projectData)

    # Check if there is another page
    nextPageTag = pageSoup.findAll('li', {'class', 'next_page'})

    if len(nextPageTag) != 0: 
        nextPageUrl = nextPageTag[0].findAll('a')[0]['href']
        if nextPageUrl.strip() != '#':
            moreProjects = await getProjectsFromPage(baseUrl, nextPageUrl)
            return projectsList + moreProjects
        else: 
            return projectsList
    else: 
        return projectsList
            

#-------------------------------------------
#   Get Hackathon Data
#-------------------------------------------
async def getHackathonData(hackathonUrl): 
    baseUrl = hackathonUrl
    projectsFromHackathon = await getProjectsFromPage(baseUrl, 'submissions/')
    return projectsFromHackathon


#-------------------------------------------
#   Main Script
#-------------------------------------------
async def main(): 

    inputFile = open("input_1.txt", "r")
    urls = inputFile.read().splitlines()

    projects = []
    for url in urls: 
        hackathonData = await getHackathonData(url)
        projects.extend(hackathonData)

    # Format data and export as CSV
    
    if len(projects) > 0: 

        with open('hackathon_projects.csv', mode='w') as csv_file:

            firstProject = projects[0]

            fieldNames = firstProject.keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
            writer.writeheader()

            for project in projects: 
                writer.writerow(project)

    totalPagesHit = 0
    for project in projects:
        totalPagesHit += 1
        totalPagesHit += project['team_member_count']

    print('Total pages hit: ' + totalPagesHit)


asyncio.run(main())