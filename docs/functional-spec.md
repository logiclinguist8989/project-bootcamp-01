
Functional Specification Document – Kukhuri-Ka
1. Project Overview

Project Name: Kukhuri-Ka: Play, Learn, and Grow Together
Target Users: Children ages 4–8, parents, and early childhood educators
Problem Statement:
Current early childhood digital learning platforms are often fragmented, difficult for pre-readers, and lack transparent progress tracking for parents and educators aligned with ECD curricula.

Project Goal:
Create a fun, safe, interactive, and curriculum-aligned gamified learning platform that develops literacy, numeracy, and social-emotional skills for children, while allowing parents to track progress.

2. Core Features (MVP)
Feature	Description	User Scenario	Inputs	Outputs	Required Screens	Priority
User Authentication	Secure login/signup for children (age-specific) and parents	A parent signs up to monitor child progress; a child logs in to play a game	Username, password, parent consent token	Login status, user session	Login, Signup	Must-have
Alphabet Adventure Module (Age 4)	Interactive letter-based learning game with sound & animation	Child selects letters to complete tasks, receives audio feedback	Letter selections, taps	Correct/incorrect feedback, progress update	Alphabet Adventure screen	Must-have
Word Builder Module (Age 5)	Interactive word formation game	Child drags letters to form words; system checks correctness	Letter selections, word submissions	Feedback, points, progress update	Word Builder screen	Must-have
Rewards System	Tracks points, unlocks badges, and displays stars	Child completes tasks → earns bananas → unlocks Gold Chicken Badge	Game activity logs	Points tally, badges earned	Rewards screen, integrated into game screens	Must-have
Child-Friendly Interface	Intuitive UI/UX with audio narration & visual cues	Child navigates the app without reading ability	Touch inputs	Navigation feedback, visual/audio cues	Main Menu, Game Screens, Navigation panels	Must-have
Parent Dashboard	Secure view of child progress and scores	Parent logs in → views child’s completed activities and scores	Parent login, child progress data	Score reports, progress charts	Parent Dashboard screen	Must-have
Privacy & Safety Compliance	Ensure safe environment, no ads, data privacy	All users use the app safely with compliance	User consent, minimal data	Privacy flags, access control	App-wide	Must-have
Dynamic Math Safari Logic	Python engine for Age 4-5 numeracy module	Child plays Math Safari → receives randomized addition problems	Number inputs	Correct/incorrect feedback, banana points, badge reward	Math Safari Screen	Must-have
3. User Scenarios

Child logs in → selects Age 4 module → completes Alphabet Adventure → earns points → receives badge notification.

Child logs in → selects Age 5 module → plays Word Builder → earns stars → progresses to next activity.

Parent logs in → views child progress → checks completed activities, scores, badges → plans offline learning.

4. Inputs & Outputs Per Feature

Inputs: User selections, touch events, number inputs, login credentials, consent token

Outputs: Visual feedback, audio cues, points tally, badges, progress percentage, score charts

5. Required Screens / Pages

Login & Signup

Main Menu / Home Screen

Alphabet Adventure Game

Word Builder Game

Rewards / Badge Screen

Parent Dashboard

Privacy & Consent Notice

6. Priority Levels
Priority	Features
Must-have	All core features above (Alphabet Adventure, Word Builder, Rewards, Parent Dashboard, Authentication, Safety)
Nice-to-have	Future modules, additional games, animations, advanced progress analytics
7. Technical Notes

Backend: Python (Math Safari module), server logic for storing progress

Frontend: Child-friendly UI, audio narration, gamified elements

GitHub Workflow: Feature-based branches, commits linked to issues

