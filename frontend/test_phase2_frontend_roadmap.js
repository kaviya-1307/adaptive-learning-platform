/**
 * Phase 2 Step 5: Frontend Roadmap & Learner Profile Visualization Test Suite
 * Validates:
 * 1. Roadmap API service loading & response contract
 * 2. Successful roadmap 4-stage progression rendering logic
 * 3. Stage status rendering (locked, available, in_progress, completed)
 * 4. Stage progress metrics & current active stage identification
 * 5. Concept-level information (mastery, weakness, confirmed gap vs neutral prior)
 * 6. Recommended problems rendering & navigation mapping
 * 7. Empty & unauthenticated (401) error states
 * 8. Strict multi-user isolation
 */

import { strict as assert } from 'assert';

const API_BASE = 'http://localhost:8000/api';

let totalChecks = 0;
let passedChecks = 0;

function check(condition, message) {
  totalChecks++;
  if (condition) {
    passedChecks++;
    console.log(`  [PASS] Check #${totalChecks}: ${message}`);
  } else {
    console.error(`  [FAIL] Check #${totalChecks}: ${message}`);
    throw new Error(`Check #${totalChecks} failed: ${message}`);
  }
}

async function runFrontendRoadmapTests() {
  console.log('=======================================================================');
  console.log('RUNNING PHASE 2 — STEP 5: FRONTEND ROADMAP & PROFILE TEST SUITE');
  console.log('=======================================================================');

  // -------------------------------------------------------------
  // 1. Unauthenticated & Error State Verification (401 Safety)
  // -------------------------------------------------------------
  console.log('\n--- [1] Roadmap API Unauthenticated & Error State Safety ---');
  const unauthRes = await fetch(`${API_BASE}/roadmap`);
  check(unauthRes.status === 401, 'Unauthenticated GET /api/roadmap rejected with 401 Unauthorized');
  const unauthData = await unauthRes.json();
  check(unauthData.detail !== undefined, '401 response includes descriptive error detail');

  // -------------------------------------------------------------
  // 2. User Registration & Initial Roadmap Loading
  // -------------------------------------------------------------
  console.log('\n--- [2] Authenticated Roadmap Loading & Schema Contract ---');
  const uid = Math.random().toString(36).substring(2, 10);
  const regRes = await fetch(`${API_BASE}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: `Frontend Tester ${uid}`,
      email: `fe_tester_${uid}@test.com`,
      password: 'Password123!'
    })
  });
  check(regRes.status === 201, 'Registered test learner for frontend roadmap verification');
  const regData = await regRes.json();
  const token = regData.access_token;
  const userId = regData.user.id;
  const authHeaders = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  };

  // Fetch roadmap
  const roadmapRes = await fetch(`${API_BASE}/roadmap`, { headers: authHeaders });
  check(roadmapRes.status === 200, 'Authenticated GET /api/roadmap returns 200 OK');
  const roadmap = await roadmapRes.json();

  check(roadmap.user_id === userId, `Roadmap user_id matches authenticated user (${roadmap.user_id} == ${userId})`);
  check(roadmap.total_stages === 4, `Roadmap contains exactly 4 stages (Got ${roadmap.total_stages})`);
  check(roadmap.stages && roadmap.stages.length === 4, 'Stages array contains exactly 4 items');
  check(roadmap.current_stage === 'Foundations', `Cold-start current_stage defaults to Foundations (Got ${roadmap.current_stage})`);
  check(roadmap.overall_progress_percent === 0.0, 'Cold-start overall progress is 0.0%');
  check(roadmap.completed_stages === 0, 'Cold-start completed stages is 0');

  // -------------------------------------------------------------
  // 3. Stage Taxonomy & Status Rendering
  // -------------------------------------------------------------
  console.log('\n--- [3] Stage Taxonomy, Prerequisites & Status Rendering ---');
  const expectedStageIds = ['stage_foundations', 'stage_data_structures', 'stage_core_algorithms', 'stage_advanced'];
  const expectedStageNames = ['Foundations', 'Data Structures', 'Core Algorithms', 'Advanced Algorithms'];

  for (let i = 0; i < 4; i++) {
    const stage = roadmap.stages[i];
    check(stage.stage_id === expectedStageIds[i], `Stage ${i + 1} ID is '${expectedStageIds[i]}'`);
    check(stage.stage_name === expectedStageNames[i], `Stage ${i + 1} Name is '${expectedStageNames[i]}'`);
    check(stage.order_index === i + 1, `Stage ${i + 1} order_index is ${i + 1}`);
    check(typeof stage.description === 'string' && stage.description.length > 20, `Stage ${i + 1} has rich pedagogical description`);
    check(['locked', 'available', 'in_progress', 'completed'].includes(stage.status), `Stage ${i + 1} status is valid enum: '${stage.status}'`);
  }

  // Foundations is unlocked for new learner
  const foundationsStage = roadmap.stages[0];
  check(foundationsStage.status === 'available' || foundationsStage.status === 'in_progress', 'Foundations stage is unlocked for new learner');
  check(foundationsStage.prerequisites.length === 0, 'Foundations stage has 0 prerequisites (Entry point)');

  // Downstream stages have correct prerequisites
  check(roadmap.stages[1].prerequisites.includes('stage_foundations'), 'Data Structures requires stage_foundations');
  check(roadmap.stages[2].prerequisites.includes('stage_data_structures'), 'Core Algorithms requires stage_data_structures');
  check(roadmap.stages[3].prerequisites.includes('stage_core_algorithms'), 'Advanced Algorithms requires stage_core_algorithms');

  // -------------------------------------------------------------
  // 4. Concept-Level Information & Prior Distinction
  // -------------------------------------------------------------
  console.log('\n--- [4] Concept-Level Information & Confirmed Gap vs Neutral Prior ---');
  let allConcepts = [];
  roadmap.stages.forEach((stage) => {
    stage.concepts.forEach((c) => allConcepts.push(c));
  });

  check(allConcepts.length === 37, `Total mapped concepts across all stages is exactly 37 (Got ${allConcepts.length})`);
  check(allConcepts.every((c) => c.concept !== '*special'), "'*special' metadata tag is strictly absent from all frontend concepts");

  // Verify cold-start concept attributes
  for (const c of allConcepts) {
    check(typeof c.concept === 'string' && c.concept.length > 0, `Concept '${c.concept}' has valid name`);
    check(c.mastery_score >= 0.0 && c.mastery_score <= 1.0, `Concept '${c.concept}' mastery in [0, 1]`);
    check(c.weakness_score >= 0.0 && c.weakness_score <= 1.0, `Concept '${c.concept}' weakness in [0, 1]`);
    check(['locked', 'available', 'in_progress', 'completed'].includes(c.status), `Concept '${c.concept}' status valid`);
  }

  // Prior distinction test: Cold-start learner has NO confirmed weaknesses
  check(allConcepts.every((c) => c.is_confirmed_weakness === false), 'Cold-start learner has 0 confirmed weaknesses (No false alarms)');
  check(allConcepts.every((c) => c.interactions === 0), 'Cold-start learner has 0 interactions on all concepts');
  check(allConcepts.every((c) => c.confidence_score === 0.0), 'Cold-start learner has 0.0 confidence across all concepts');

  // -------------------------------------------------------------
  // 5. Diagnostic Calibration & Dynamic Progression Reflection
  // -------------------------------------------------------------
  console.log('\n--- [5] Diagnostic Calibration & Dynamic Progression Reflection ---');
  // Submit diagnostic attempts:
  // Problem #1 (Two Sum: 'hashing', 'data structures') -> Solved
  const sub1 = await fetch(`${API_BASE}/diagnostic/submit`, {
    method: 'POST',
    headers: authHeaders,
    body: JSON.stringify({
      problem_id: 1,
      is_solved: true,
      time_spent_seconds: 45,
      code_submitted: 'def solution(): return True'
    })
  });
  check(sub1.status === 200, 'Submitted diagnostic attempt #1 (Solved)');

  // Problem #6 (Valid Anagram: 'strings', 'hashing') -> Solved
  const sub2 = await fetch(`${API_BASE}/diagnostic/submit`, {
    method: 'POST',
    headers: authHeaders,
    body: JSON.stringify({
      problem_id: 6,
      is_solved: true,
      time_spent_seconds: 50,
      code_submitted: 'def solution(): return True'
    })
  });
  check(sub2.status === 200, 'Submitted diagnostic attempt #6 (Solved)');

  // Problem #33 (Climbing Stairs: 'dp') -> Failed
  const sub3 = await fetch(`${API_BASE}/diagnostic/submit`, {
    method: 'POST',
    headers: authHeaders,
    body: JSON.stringify({
      problem_id: 33,
      is_solved: false,
      time_spent_seconds: 120,
      code_submitted: 'def solution(): pass'
    })
  });
  check(sub3.status === 200, 'Submitted diagnostic attempt #33 (Failed DP)');

  // Complete diagnostic
  const compRes = await fetch(`${API_BASE}/diagnostic/complete`, {
    method: 'POST',
    headers: authHeaders
  });
  check(compRes.status === 200, 'Completed diagnostic assessment');

  // Re-fetch calibrated roadmap
  const calRoadmapRes = await fetch(`${API_BASE}/roadmap`, { headers: authHeaders });
  check(calRoadmapRes.status === 200, 'Fetched calibrated roadmap post-diagnostic');
  const calRoadmap = await calRoadmapRes.json();

  // Verify Hashing concept in Foundations: Solved 2/2 -> Mastery 0.75, Conf 0.20 -> Mastered
  const calFoundations = calRoadmap.stages.find((s) => s.stage_id === 'stage_foundations');
  const hashingConcept = calFoundations.concepts.find((c) => c.concept === 'hashing');
  check(hashingConcept.mastery_score === 0.75, `Hashing mastery boosted to 0.75 (Got ${hashingConcept.mastery_score})`);
  check(hashingConcept.weakness_score === 0.25, `Hashing weakness dropped to 0.25 (Got ${hashingConcept.weakness_score})`);
  check(hashingConcept.status === 'completed', `Hashing status rendered as 'completed' (Got ${hashingConcept.status})`);
  check(hashingConcept.is_confirmed_weakness === false, 'Mastered hashing is NOT flagged as confirmed weakness');

  // Verify DP concept in Advanced: Failed 0/1 -> Mastery 0.3333, Weakness 0.6667, Conf 0.10 -> Confirmed Weakness
  const calAdvanced = calRoadmap.stages.find((s) => s.stage_id === 'stage_advanced');
  const dpConcept = calAdvanced.concepts.find((c) => c.concept === 'dp');
  check(Math.abs(dpConcept.mastery_score - 0.3333) < 1e-3, `DP mastery dropped to 0.3333 on failure (Got ${dpConcept.mastery_score})`);
  check(Math.abs(dpConcept.weakness_score - 0.6667) < 1e-3, `DP weakness elevated to 0.6667 (Got ${dpConcept.weakness_score})`);
  check(dpConcept.is_confirmed_weakness === true, 'DP explicitly flagged as is_confirmed_weakness == true');
  check(dpConcept.priority === 1, 'DP prioritized as #1 learning urgency within Advanced stage');
  check(dpConcept.weakness_level === 'Very High', `DP weakness_level is 'Very High' (Got ${dpConcept.weakness_level})`);

  // Verify untested concept (e.g. 'graphs') retains neutral prior
  const calCore = calRoadmap.stages.find((s) => s.stage_id === 'stage_core_algorithms');
  const graphsConcept = calCore.concepts.find((c) => c.concept === 'graphs');
  check(graphsConcept.interactions === 0, 'Untested graphs interactions == 0');
  check(graphsConcept.mastery_score === 0.50, 'Untested graphs mastery == 0.50 (neutral prior)');
  check(graphsConcept.is_confirmed_weakness === false, 'Untested graphs is NOT classified as confirmed weakness');

  // Verify stage progress percent update
  check(calFoundations.completed_concepts >= 1, `Foundations has >= 1 completed concept (Got ${calFoundations.completed_concepts})`);
  check(calFoundations.progress_percent > 0.0, `Foundations progress percent updated dynamically (Got ${calFoundations.progress_percent}%)`);

  // -------------------------------------------------------------
  // 6. Recommended Problems Rendering & Navigation Mapping
  // -------------------------------------------------------------
  console.log('\n--- [6] Recommended Problems Rendering & Navigation Mapping ---');
  // Fetch problems catalog to ensure every recommended problem ID maps to real problem
  const probsRes = await fetch(`${API_BASE}/problems`);
  check(probsRes.status === 200, 'Fetched problems catalog for frontend navigation mapping');
  const allProblems = await probsRes.json();
  const problemCatalogMap = new Map(allProblems.map((p) => [p.id, p]));

  for (const stage of calRoadmap.stages) {
    check(Array.isArray(stage.recommended_problem_ids), `Stage ${stage.stage_name} includes recommended_problem_ids list`);
    for (const pid of stage.recommended_problem_ids) {
      const realProblem = problemCatalogMap.get(pid);
      check(realProblem !== undefined, `Recommended problem ID ${pid} resolves to real problem in catalog`);
      check(typeof realProblem.slug === 'string' && realProblem.slug.length > 0, `Problem ID ${pid} has slug for navigation ('${realProblem.slug}')`);
      check(typeof realProblem.title === 'string' && realProblem.title.length > 0, `Problem ID ${pid} has title ('${realProblem.title}')`);
      check(['Easy', 'Medium', 'Hard'].includes(realProblem.difficulty), `Problem ID ${pid} has valid difficulty ('${realProblem.difficulty}')`);
    }
  }

  // -------------------------------------------------------------
  // 7. Multi-User Isolation & Privacy Verification
  // -------------------------------------------------------------
  console.log('\n--- [7] Multi-User Isolation & Privacy Verification ---');
  const uid2 = Math.random().toString(36).substring(2, 10);
  const reg2Res = await fetch(`${API_BASE}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: `User Two ${uid2}`,
      email: `u2_${uid2}@test.com`,
      password: 'Password123!'
    })
  });
  const reg2Data = await reg2Res.json();
  const token2 = reg2Data.access_token;
  const user2Id = reg2Data.user.id;

  const roadmap2Res = await fetch(`${API_BASE}/roadmap`, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token2}`
    }
  });
  check(roadmap2Res.status === 200, 'User 2 fetched independent roadmap');
  const roadmap2 = await roadmap2Res.json();
  check(roadmap2.user_id === user2Id, `User 2 roadmap strictly isolated (${roadmap2.user_id} == ${user2Id})`);

  // User 2 must NOT have Hashing completed
  const u2Foundations = roadmap2.stages.find((s) => s.stage_id === 'stage_foundations');
  const u2Hashing = u2Foundations.concepts.find((c) => c.concept === 'hashing');
  check(u2Hashing.status === 'available', `User 2 hashing status is 'available', isolated from User 1 completed state`);
  check(u2Hashing.interactions === 0, 'User 2 hashing interactions == 0');
  check(roadmap2.overall_progress_percent === 0.0, 'User 2 overall progress is 0.0% (No state leakage)');

  console.log('\n=======================================================================');
  console.log(`PHASE 2 STEP 5 FRONTEND TEST SUMMARY: ALL ${passedChecks}/${totalChecks} CHECKS PASSED (100% SUCCESS)`);
  console.log('=======================================================================');
}

runFrontendRoadmapTests().catch((err) => {
  console.error('\n[FATAL] Test execution failed:', err);
  process.exit(1);
});
