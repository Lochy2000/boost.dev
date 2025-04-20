#Progression System

## Overview

Boost.dev includes a progression system that rewards users for their activities. This document explains how the points, levels, and achievements work in the application.

## Points System

Users earn points for various activities:
- Logging a daily win: +20 points
- Completing a beginner challenge: +30 points
- Completing an intermediate challenge: +45 points
- Completing a hard challenge: +60 points
- Creating a challenge: +40 points
- Updating profile: +15 points

## Level System

The app has 5 levels with different point thresholds:

| Level | Title | Points Required |
|-------|-------|----------------|
| 1 | Rookie | 0 - 29 |
| 2 | Explorer | 30 - 69 |
| 3 | Hacker | 70 - 119 |
| 4 | Wizard | 120 - 199 |
| 5 | Master | 200+ |

When a user reaches enough points, they level up automatically. Level progress is shown as a percentage in the UI.

## Achievements

Achievements are awarded for specific actions or milestones:

- **Level Achievements**: Given when reaching a new level (e.g., "Level 1 Rookie", "Level 2 Explorer")
- **Activity Achievements**:
  - "First Win": Awarded after logging the first daily win
  - "Challenge Accepted": Awarded after completing the first challenge
  - "Challenge Creator": Awarded after creating a challenge
  - "Fast Learner": Awarded when reaching level 3
  - "Early Adopter": Awarded when updating profile
  - "Hackathon Hero": Special achievement for the hackathon

## functionality

1. **User Progress Model**
   - The `UserProgress` model tracks points, current level, and next level threshold
   - Each user has one UserProgress instance created when they register

2. **Points and Leveling Logic**
   - When users perform actions, `add_user_points()` function is called
   - This updates points and calls `update_level()` to check if the user leveled up
   - If user levels up, `award_level_achievement()` is called

3. **Achievement System**
   - Achievements are stored in the `Achievement` model
   - When a user earns an achievement, a `UserAchievement` record is created
   - Achievements can be triggered by direct actions or by level-ups

4. **Notification System**
   - Level-up notifications use a combination of Django messages and UserFlags
   - Achievements display toast notifications via JavaScript
   - Both use the same UI components for consistency


