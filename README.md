# IMPACT_API

## Overview
A Django-based API that modernises ESL (English as a Second Language) student assessment management. This system digitises the traditional Records of Results (ROR) process, replacing individual Word documents with a centralised, accessible database solution.

## Problem Statement
Current ESL assessment tracking relies on individual Word documents per student, creating several challenges:
- Limited accessibility (local access only)
- Time-consuming manual data entry
- Difficult to track trends across classes or identify patterns
- No automated analysis of teaching effectiveness
- Challenging to monitor student progress in real-time

## Solution
IMPACT_API provides:
- Centralised database for student Records of Results
- Real-time access to student performance data
- Automated grade calculations
- Tracking system for 7 key skills:
  - Grammar
  - Vocabulary
  - Listening
  - Reading
  - Writing
  - Speaking
  - Pronunciation
- Analytics for identifying:
  - Stagnant or declining performance
  - Teaching effectiveness metrics
  - Class-wide trends

## Technical Features
- Full CRUD operations for:
  - Classes
  - Teachers
  - Students
  - Test Results
- Automated grade calculations based on standardised conversion table
- Week-by-week progress tracking
- Overall assessment compilation

## Roadmap

### Phase 1: Core API Foundation
- [x] Initial project setup
- [ ] Authentication system implementation
  - [ ] JWT authentication
  - [ ] User roles (admin, teachers)
  - [ ] Permission settings
- [ ] Core models development
  - [ ] Student model
  - [ ] Class model
  - [ ] Teacher model
  - [ ] Test model
  - [ ] Database relationships

### Phase 2: Assessment Features
- [ ] Grade calculation system
  - [ ] Percentage to grade conversion
  - [ ] Overall assessment calculations
- [ ] Test results management
  - [ ] Weekly test entry endpoints
  - [ ] Progress monitoring

### Phase 3: Frontend Development
- [ ] React frontend application
  - [ ] User authentication interface
  - [ ] Dashboard views
  - [ ] Test result entry forms
  - [ ] Student progress views

### Future Enhancements
- [ ] Export functionality
  - [ ] Generate ROR documents in standard format
  - [ ] Batch export capabilities
- [ ] Data visualisation
  - [ ] Student progress graphs
  - [ ] Class performance analytics
  - [ ] Teaching effectiveness metrics
- [ ] Additional features
  - [ ] Email notifications
  - [ ] Batch data import
  - [ ] Mobile responsiveness