# User Evaluation Plan

## Objective

Evaluate the effectiveness of the Movie Information Retrieval system by comparing a baseline interface (basic search only) with the full interface (including faceted search and More Like This features).

## Research Questions

1. Does faceted search improve task completion rates and reduce time to find relevant movies?
2. Does the More Like This feature help users discover relevant movies they wouldn't find through keyword search?
3. What is the overall user satisfaction with the system?

## Methodology

### Participants

- **Target**: 10-15 participants (students, movie enthusiasts)
- **Recruitment**: Class colleagues, social media, movie clubs
- **Criteria**: Participants should have basic movie knowledge and use search engines regularly

### Experimental Design

**Between-subjects design** with two conditions:

1. **Baseline Group**: Access to basic search interface only
   - Search box with keyword search
   - Results list with pagination
   - No filters or similar movies feature

2. **Full System Group**: Access to complete interface
   - Basic search
   - Faceted filters (genre, year, rating)
   - More Like This feature
   - All advanced IR features

Each participant will be randomly assigned to one condition.

### Tasks

Participants will complete 5 search tasks designed to test different aspects of the system:

#### Task 1: Simple Known-Item Search
**"Find the movie 'Inception' and note its rating."**

- **Type**: Simple lookup
- **Measures**: Time to completion, success rate
- **Tests**: Basic search effectiveness

#### Task 2: Faceted Search Task
**"Find a highly-rated (8.0+) science fiction movie released after 2010."**

- **Type**: Multi-criteria search
- **Measures**: Time, number of queries, success rate
- **Tests**: Faceted filtering effectiveness

#### Task 3: Genre Exploration
**"Find 3 comedy movies from the 1990s with ratings above 7.0."**

- **Type**: Exploratory search with constraints
- **Measures**: Time, number of queries, result quality
- **Tests**: Combined filtering and browsing

#### Task 4: Discovery Task
**"Find a movie similar to 'The Dark Knight' that you haven't seen before."**

- **Type**: Recommendation/similarity-based
- **Measures**: Time, satisfaction with recommendations
- **Tests**: More Like This feature

#### Task 5: Complex Information Need
**"Find a family-friendly animated movie from the last 5 years with at least a 7.5 rating. The movie should feature adventure themes."**

- **Type**: Complex multi-faceted search
- **Measures**: Time, queries, success, satisfaction
- **Tests**: Overall system effectiveness

### Data Collection

For each task, collect:

1. **Performance Metrics**:
   - Task completion success (Yes/No)
   - Time to complete task (seconds)
   - Number of queries submitted
   - Number of result pages viewed
   - Number of filters applied (full system only)
   - Use of More Like This feature (full system only)

2. **Subjective Measures** (post-task questionnaire):
   - Task difficulty (1-5 scale)
   - Confidence in result (1-5 scale)
   - Satisfaction with search process (1-5 scale)

3. **Overall System Evaluation** (post-session questionnaire):
   - Ease of use (1-5 scale)
   - Usefulness of features (1-5 scale, per feature)
   - Overall satisfaction (1-5 scale)
   - Open-ended feedback

### Procedure

1. **Introduction** (5 minutes)
   - Explain study purpose
   - Obtain consent
   - Brief system tutorial

2. **Task Session** (20-30 minutes)
   - Complete 5 tasks in order
   - Think-aloud protocol (encouraged but optional)
   - Record all metrics

3. **Post-Session Questionnaire** (5 minutes)
   - Overall system evaluation
   - Feature preferences
   - Suggestions for improvement

4. **Debrief** (5 minutes)
   - Answer questions
   - Thank participant

**Total time per participant**: ~40 minutes

### Materials Needed

- Laptop with browser access to the system
- Screen recording software (optional)
- Timer
- Data collection spreadsheet
- Consent form
- Task instruction sheets
- Questionnaires (printed or digital)

## Data Analysis Plan

### Quantitative Analysis

1. **Task Completion Rate**
   - Compare success rates between baseline and full system
   - Statistical test: Chi-square test or Fisher's exact test

2. **Task Completion Time**
   - Compare average time per task
   - Statistical test: Independent t-test or Mann-Whitney U test

3. **Search Efficiency**
   - Number of queries per task
   - Number of pages viewed
   - Statistical test: Independent t-test

4. **User Satisfaction**
   - Compare ratings across conditions
   - Statistical test: Independent t-test for each scale item

### Qualitative Analysis

- Thematic analysis of open-ended feedback
- Identify common usability issues
- Extract feature preferences and suggestions

### Expected Outcomes

**Hypotheses**:

1. **H1**: The full system will have higher task completion rates than baseline for Tasks 2-5
2. **H2**: The full system will reduce task completion time for Tasks 2-5
3. **H3**: Users of the full system will report higher satisfaction scores
4. **H4**: The More Like This feature will be rated as useful for discovery tasks

## Evaluation Metrics Summary

| Metric | Measurement Method | Scale |
|--------|-------------------|-------|
| Task Success | Binary (completed/failed) | Yes/No |
| Time to Complete | Stopwatch | Seconds |
| Number of Queries | Count | Integer |
| Pages Viewed | Count | Integer |
| Filters Used | Count | Integer |
| Task Difficulty | Likert scale | 1-5 |
| Confidence in Result | Likert scale | 1-5 |
| Task Satisfaction | Likert scale | 1-5 |
| System Ease of Use | Likert scale | 1-5 |
| Feature Usefulness | Likert scale | 1-5 |
| Overall Satisfaction | Likert scale | 1-5 |

## Ethical Considerations

- Obtain informed consent from all participants
- Ensure anonymity in data reporting
- Allow participants to withdraw at any time
- No sensitive personal information collected
- Results used for educational purposes only

## Timeline

- Week 1: Finalize evaluation materials and recruit participants
- Week 2: Conduct user sessions (5-7 participants per day)
- Week 3: Data analysis and report writing
- Week 4: Present findings in final report

## Limitations

- Small sample size (convenience sampling)
- Limited task variety
- Short-term evaluation (no longitudinal data)
- Single domain (movies only)
- Self-reported measures subject to bias

## References

For evaluation methodology inspiration:
- Kelly, D. (2009). Methods for evaluating interactive information retrieval systems with users.
- Borlund, P. (2003). The concept of relevance in IR.
- ISO 9241-11: Ergonomics of human-system interaction - Usability definitions and concepts.
