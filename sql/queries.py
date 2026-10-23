QUERIES = {
1: {"level": "Beginner", "title": "Indian Players",
    "sql": "SELECT name, role, batting_style, bowling_style FROM players WHERE country='India'"},
2: {"level": "Beginner", "title": "Matches in Last 30 Days",
    "sql": """SELECT m.description, m.team1, m.team2, v.name||', '||v.city AS venue,
              m.match_date FROM matches m JOIN venues v ON m.venue_id=v.venue_id
              WHERE m.match_date >= date('now','-30 days') ORDER BY m.match_date DESC"""},
3: {"level": "Beginner", "title": "Top 10 ODI Run Scorers",
    "sql": """SELECT p.name, SUM(s.runs) AS total_runs,
              ROUND(AVG(s.runs),2) AS avg_runs, COUNT(CASE WHEN s.runs>=100 THEN 1 END) AS centuries
              FROM player_stats s JOIN players p ON s.player_id=p.player_id
              WHERE s.format='ODI' GROUP BY p.player_id ORDER BY total_runs DESC LIMIT 10"""},
4: {"level": "Beginner", "title": "Large Venues",
    "sql": "SELECT name, city, country, capacity FROM venues WHERE capacity>50000 ORDER BY capacity DESC"},
5: {"level": "Beginner", "title": "Matches Won per Team",
    "sql": """SELECT winner AS team, COUNT(*) AS wins FROM matches
              WHERE winner IS NOT NULL GROUP BY winner ORDER BY wins DESC"""},
6: {"level": "Beginner", "title": "Players per Role",
    "sql": "SELECT role, COUNT(*) AS player_count FROM players GROUP BY role ORDER BY player_count DESC"},
7: {"level": "Beginner", "title": "Highest Score per Format",
    "sql": "SELECT format, MAX(runs) AS highest_score FROM player_stats GROUP BY format"},
8: {"level": "Beginner", "title": "Series Started in 2024",
    "sql": """SELECT description AS series_name, team1 AS host, 'T20' AS match_type,
              MIN(match_date) AS start_date, COUNT(*) AS total_matches
              FROM matches WHERE strftime('%Y', match_date)='2024' GROUP BY description"""},
9: {"level": "Intermediate", "title": "All-Rounders (1000+ runs, 50+ wickets)",
    "sql": """SELECT p.name, SUM(s.runs) AS total_runs, SUM(s.wickets) AS total_wickets, s.format
              FROM player_stats s JOIN players p ON s.player_id=p.player_id
              GROUP BY p.player_id, s.format
              HAVING SUM(s.runs)>1000 AND SUM(s.wickets)>50"""},
10: {"level": "Intermediate", "title": "Last 20 Completed Matches",
     "sql": """SELECT m.description, m.team1, m.team2, m.winner, m.victory_margin,
               m.victory_type, v.name AS venue FROM matches m
               JOIN venues v ON m.venue_id=v.venue_id
               WHERE m.winner IS NOT NULL ORDER BY m.match_date DESC LIMIT 20"""},
11: {"level": "Intermediate", "title": "Player Performance Across Formats",
     "sql": """SELECT p.name,
               SUM(CASE WHEN s.format='Test' THEN s.runs ELSE 0 END) AS test_runs,
               SUM(CASE WHEN s.format='ODI' THEN s.runs ELSE 0 END) AS odi_runs,
               SUM(CASE WHEN s.format='T20I' THEN s.runs ELSE 0 END) AS t20_runs,
               ROUND(AVG(s.runs),2) AS overall_avg
               FROM player_stats s JOIN players p ON s.player_id=p.player_id
               GROUP BY p.player_id HAVING COUNT(DISTINCT s.format)>=2"""},
12: {"level": "Intermediate", "title": "Home vs Away Performance",
     "sql": """SELECT p.country AS team,
               SUM(CASE WHEN v.country=p.country AND m.winner=p.country THEN 1 ELSE 0 END) AS home_wins,
               SUM(CASE WHEN v.country!=p.country AND m.winner=p.country THEN 1 ELSE 0 END) AS away_wins
               FROM players p, matches m JOIN venues v ON m.venue_id=v.venue_id
               WHERE p.name=m.winner GROUP BY p.country"""},
13: {"level": "Intermediate", "title": "Partnerships 100+ Runs",
     "sql": """SELECT p1.name AS batsman1, p2.name AS batsman2,
               (s1.runs+s2.runs) AS partnership_runs, s1.match_id
               FROM player_stats s1 JOIN player_stats s2
               ON s1.match_id=s2.match_id AND s1.player_id<s2.player_id
               JOIN players p1 ON s1.player_id=p1.player_id
               JOIN players p2 ON s2.player_id=p2.player_id
               WHERE (s1.runs+s2.runs)>=100"""},
14: {"level": "Intermediate", "title": "Bowling at Venues (3+ matches)",
     "sql": """SELECT p.name, v.name AS venue,
               ROUND(SUM(s.runs_conceded)/NULLIF(SUM(s.overs_bowled),0),2) AS economy,
               SUM(s.wickets) AS wickets, COUNT(*) AS matches
               FROM player_stats s JOIN players p ON s.player_id=p.player_id
               JOIN matches m ON s.match_id=m.match_id JOIN venues v ON m.venue_id=v.venue_id
               GROUP BY p.player_id, v.venue_id HAVING COUNT(*)>=3"""},
15: {"level": "Intermediate", "title": "Close Match Performers",
     "sql": """SELECT p.name, ROUND(AVG(s.runs),2) AS avg_runs, COUNT(*) AS close_matches,
               SUM(CASE WHEN m.winner=m.team1 OR m.winner=m.team2 THEN 1 ELSE 0 END) AS team_wins
               FROM player_stats s JOIN players p ON s.player_id=p.player_id
               JOIN matches m ON s.match_id=m.match_id
               WHERE m.victory_type='runs' AND CAST(m.victory_margin AS INTEGER)<50
               GROUP BY p.player_id"""},
16: {"level": "Intermediate", "title": "Yearly Batting Trends",
     "sql": """SELECT p.name, strftime('%Y', m.match_date) AS year,
               ROUND(AVG(s.runs),2) AS avg_runs,
               ROUND(AVG(CASE WHEN s.balls_faced>0 THEN s.runs*100.0/s.balls_faced END),2) AS avg_sr
               FROM player_stats s JOIN players p ON s.player_id=p.player_id
               JOIN matches m ON s.match_id=m.match_id
               WHERE m.match_date>='2020-01-01'
               GROUP BY p.player_id, year HAVING COUNT(*)>=5"""},
17: {"level": "Advanced", "title": "Toss Advantage",
     "sql": """SELECT toss_decision,
               COUNT(*) AS total,
               SUM(CASE WHEN toss_winner=winner THEN 1 ELSE 0 END) AS toss_win_matches,
               ROUND(100.0*SUM(CASE WHEN toss_winner=winner THEN 1 ELSE 0 END)/COUNT(*),2) AS win_pct
               FROM matches WHERE winner IS NOT NULL GROUP BY toss_decision"""},
18: {"level": "Advanced", "title": "Economical Bowlers (10+ matches)",
     "sql": """SELECT p.name, ROUND(SUM(s.runs_conceded)/NULLIF(SUM(s.overs_bowled),0),2) AS economy,
               SUM(s.wickets) AS wickets FROM player_stats s JOIN players p ON s.player_id=p.player_id
               WHERE s.format IN ('ODI','T20') GROUP BY p.player_id
               HAVING COUNT(*)>=10 AND AVG(s.overs_bowled)>=2 ORDER BY economy ASC"""},
19: {"level": "Advanced", "title": "Consistent Batsmen",
     "sql": """SELECT p.name, ROUND(AVG(s.runs),2) AS avg_runs,
               ROUND(STDEV(s.runs),2) AS std_dev FROM player_stats s JOIN players p ON s.player_id=p.player_id
               JOIN matches m ON s.match_id=m.match_id
               WHERE m.match_date>='2022-01-01' AND s.balls_faced>=10
               GROUP BY p.player_id ORDER BY std_dev ASC"""},
20: {"level": "Advanced", "title": "Matches & Avg per Format (20+ total)",
     "sql": """SELECT p.name,
               COUNT(CASE WHEN s.format='Test' THEN 1 END) AS test_matches,
               COUNT(CASE WHEN s.format='ODI' THEN 1 END) AS odi_matches,
               COUNT(CASE WHEN s.format='T20I' THEN 1 END) AS t20_matches,
               ROUND(AVG(s.runs),2) AS overall_avg
               FROM player_stats s JOIN players p ON s.player_id=p.player_id
               GROUP BY p.player_id HAVING COUNT(*)>=20"""},
21: {"level": "Advanced", "title": "Player Ranking System",
     "sql": """SELECT p.name, s.format,
               ROUND(SUM(s.runs)*0.01 + AVG(s.runs)*0.5 + AVG(CASE WHEN s.balls_faced>0 THEN s.runs*100.0/s.balls_faced END)*0.3
               + SUM(s.wickets)*2 + (50 - AVG(s.runs_conceded/NULLIF(s.overs_bowled,0)))*0.5
               + (6 - AVG(s.runs_conceded/NULLIF(s.overs_bowled,0)))*2
               + SUM(s.catches)*3 + SUM(s.stumpings)*5, 2) AS total_points
               FROM player_stats s JOIN players p ON s.player_id=p.player_id
               GROUP BY p.player_id, s.format ORDER BY total_points DESC"""},
22: {"level": "Advanced", "title": "Head-to-Head Analysis",
     "sql": """SELECT team1, team2, COUNT(*) AS matches_played,
               SUM(CASE WHEN winner=team1 THEN 1 ELSE 0 END) AS team1_wins,
               SUM(CASE WHEN winner=team2 THEN 1 ELSE 0 END) AS team2_wins
               FROM matches WHERE match_date>=date('now','-3 years') AND winner IS NOT NULL
               GROUP BY team1, team2 HAVING COUNT(*)>=5"""},
23: {"level": "Advanced", "title": "Recent Form (Last 10)",
     "sql": """WITH recent AS (
               SELECT s.player_id, s.runs, s.balls_faced,
               ROW_NUMBER() OVER (PARTITION BY s.player_id ORDER BY m.match_date DESC) AS rn
               FROM player_stats s JOIN matches m ON s.match_id=m.match_id)
               SELECT p.name, ROUND(AVG(CASE WHEN rn<=5 THEN runs END),2) AS avg_last5,
               ROUND(AVG(runs),2) AS avg_last10,
               SUM(CASE WHEN runs>=50 THEN 1 ELSE 0 END) AS scores_above_50
               FROM recent r JOIN players p ON r.player_id=p.player_id
               WHERE rn<=10 GROUP BY p.player_id"""},
24: {"level": "Advanced", "title": "Best Batting Partnerships",
     "sql": """WITH pairs AS (
               SELECT s1.player_id AS p1, s2.player_id AS p2, s1.match_id,
               s1.runs+s2.runs AS partnership
               FROM player_stats s1 JOIN player_stats s2
               ON s1.match_id=s2.match_id AND s1.player_id<s2.player_id)
               SELECT pl1.name, pl2.name, COUNT(*) AS partnerships,
               ROUND(AVG(partnership),2) AS avg_partnership,
               SUM(CASE WHEN partnership>50 THEN 1 ELSE 0 END) AS good_partnerships,
               MAX(partnership) AS highest
               FROM pairs JOIN players pl1 ON pairs.p1=pl1.player_id
               JOIN players pl2 ON pairs.p2=pl2.player_id
               GROUP BY p1,p2 HAVING COUNT(*)>=5 ORDER BY avg_partnership DESC"""},
25: {"level": "Advanced", "title": "Career Trajectory (6+ quarters)",
     "sql": """WITH quarterly AS (
               SELECT s.player_id, strftime('%Y-Q', m.match_date) AS quarter,
               AVG(s.runs) AS avg_runs, COUNT(*) AS matches
               FROM player_stats s JOIN matches m ON s.match_id=m.match_id
               GROUP BY s.player_id, quarter HAVING COUNT(*)>=3)
               SELECT p.name, q.quarter, ROUND(q.avg_runs,2) AS avg_runs,
               ROUND(q.avg_runs - LAG(q.avg_runs) OVER (PARTITION BY q.player_id ORDER BY q.quarter),2) AS change
               FROM quarterly q JOIN players p ON q.player_id=p.player_id
               WHERE q.player_id IN (SELECT player_id FROM quarterly GROUP BY player_id HAVING COUNT(*)>=6)"""}
}
