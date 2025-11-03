# Type-1: Planning and Acting for Least-Effort Biking Routes in a City Grid

**Course:** CMSC 722: AI Planning
**Term:** Fall 2025  

**Author:**  
Huan Zhou  
[hzhou715@umd.edu](mailto:hzhou715@umd.edu)

**Instructor:**  
Dr. Mak Roberts
David Chan

---

## 1. Project overview

This project evaluates least-effort biking on a city grid using a classical PDDL planner with action costs. Each grid cell encodes terrain difficulty; moving into a cell adds its cost to the plan. The planner minimizes total cost to reach the goal, and an acting loop executes the plan.

We will use an existing grid simulator (e.g., SimpleGrid or POSGGym GridWorld) rather than building one from scratch. A small translator will export the simulator state to PDDL (objects, adjacency, per-cell costs) and import the resulting plan back into the simulator. This keeps modeling simple and leverages classical planners’ strength at path search. 

Research question. How does terrain difficulty, represented as action cost, affect planning and acting performance?

Comparison. We compare Run-Lookahead and Run-Lazy-Lookahead on planning time, total effort, plan length, and number of replans. We expect Run-Lookahead to replan more and achieve lower total cost, while Run-Lazy-Lookahead plans faster but may yield higher cost.

---

## 2. Methods

### 2.1 System Overview

- Planner: a classical PDDL planner, an existing grid simulator (e.g., SimpleGrid or POSGGym GridWorld)
- Acting: Run-Lookahead vs Run-Lazy-Lookahead
- Metrics: planning time, total effort, plan length, replans




