# MindCare Demo Video Script
## 3-Minute Demonstration Guide

**Project**: Advanced HCI 2025-2026  
**Topic**: MindCare - Mental Well-being Monitoring System  
**Duration**: 3 minutes maximum

---

## Script Structure

### Introduction (0:00 - 0:30)

**Visual**: Title slide with MindCare logo, transition to presenter

**Narration**:
> "Hello! I'm presenting MindCare, an intelligent mental well-being monitoring system designed for the Advanced HCI course. MindCare addresses a critical problem: many people don't recognize early signs of stress and anxiety until symptoms become severe. Our solution uses facial expression recognition with multimodal interaction to provide passive, real-time emotional awareness."

**Key Points to Show**:
- Project name and topic
- Brief problem statement
- Solution overview

---

### Part I: Problem and Multimodal Solution (0:30 - 1:15)

**Visual**: Slides showing problem definition, ARCADE framework diagram

**Narration**:
> "The problem: individuals lack self-awareness of gradual emotional changes, leading to delayed intervention. Traditional mental health services have accessibility barriers and are reactive rather than proactive."
>
> "MindCare implements multimodal interaction following the ARCADE framework:
> - **Camera** for passive facial expression monitoring
> - **Voice** for hands-free commands
> - **Touch** interface for detailed configuration
>
> These modalities provide Assignment, Redundancy, Complementarity, and Equivalence. For example, you can check your mood either by saying 'How am I doing?' or clicking the dashboard button."

**Key Visuals**:
- Problem statistics/quotes
- Multimodal interaction diagram
- ARCADE framework application

**Transitions**: Pros and cons briefly mentioned
> "Key advantages include non-intrusive monitoring and early warning capabilities. Main challenges are privacy concerns and accuracy limitations, which we address through local processing and appropriate user expectations."

---

### Part II: User Design and System Architecture (1:15 - 2:00)

**Visual**: Persona slide, scenario storyboard, UML Component Diagram

**Narration**:
> "Meet Maria, our persona—a 28-year-old software developer experiencing workplace stress. Our scenario shows how MindCare detects her stress patterns during a typical workday and suggests timely breaks."
>
> "The system architecture features four layers:
> - **Interface Layer**: PyQt5 GUI with voice and notifications
> - **Application Layer**: FSM controller managing system behavior
> - **Processing Layer**: OpenCV for face detection, CNN for emotion classification with time-window aggregation
> - **Data Layer**: Encrypted local database
>
> All processing happens on-device for privacy."

**Key Visuals**:
- Persona profile (key details)
- Scenario timeline (2-3 key moments)
- UML Component Diagram (simplified)
- Technical specs table

---

### Part III: Live Demonstration (2:00 - 2:45)

**Visual**: Screen recording of application running

**Narration**:
> "Now let me demonstrate the implementation. Starting the application..."

**Demo Steps** (pre-recorded screen capture):

1. **Initialization** (0:00-0:05)
   - Show console output: "Loading face detector... Loading emotion classifier... ✓ Initialization complete"
   - "The system initializes the face detector and CNN emotion classifier"

2. **Real-time Monitoring** (0:05-0:25)
   - Camera feed shows face with colored bounding box
   - Console prints: `[14:23:15] Emotion: NEUTRAL | Confidence: 0.78 | Valence: +0.02`
   - "The system detects my face and classifies emotions in real-time. Notice the colored bounding box."
   - Change expression (try smiling): box color changes, emotion updates
   - "Predictions are aggregated over 2-second sliding windows to reduce noise"

3. **Time-Window Processing** (0:25-0:30)
   - Console shows multiple emotion readings
   - "Each second, the system logs the aggregated emotion from the last 60 frames"

4. **Stress Pattern Detection** (0:30-0:40)
   - (If possible, show pre-recorded stress pattern)
   - Console displays: 
     ```
     ⚠️  STRESS PATTERN DETECTED
        Negative emotions: 65.0% over last 20 readings
        Suggestion: Consider taking a short break
     ```
   - "Every 30 seconds, the system analyzes the last 15 minutes. When stress exceeds 60%, it alerts the user."

5. **Session Summary** (0:40-0:45)
   - Press 'q' to quit
   - Show session summary with emotion distribution chart
   - "Upon exit, users see their emotional distribution and average valence."

**Narration During Demo**:
> "The implementation demonstrates key functionality: real-time facial expression detection using OpenCV Haar Cascades, CNN-based emotion classification, time-window data processing over 2-second intervals, and pattern-based stress detection every 30 seconds."

---

### Conclusion (2:45 - 3:00)

**Visual**: Summary slide, return to presenter

**Narration**:
> "In summary, MindCare demonstrates how multimodal HCI can address mental well-being through:
> - Passive monitoring that respects user privacy
> - Real-time emotional awareness with time-windowed accuracy
> - Proactive stress detection and intervention suggestions
>
> While this is a prototype with limitations—including the need for better-trained models—it establishes a foundation for non-intrusive mental health support tools that complement professional services."
>
> "Thank you! I'm happy to answer questions."

**Final Slide**: 
- Contact information
- Links to code repository (if applicable)
- "Questions?" prompt

---

## Recording Tips

### Before Recording

1. **Test Everything**:
   - Run `python src/main.py` multiple times to ensure stability
   - Verify camera works and lighting is good
   - Practice narration to stay within 3 minutes

2. **Prepare Slides**:
   - Create 5-7 concise slides in PowerPoint/Keynote
   - Keep text minimal, use visuals (diagrams, screenshots)
   - Include: Title, Problem, Solution (ARCADE), Persona+Architecture, Demo (blank for live), Conclusion

3. **Screen Recording Setup**:
   - Use OBS Studio, QuickTime, or similar
   - Set resolution to 1920x1080
   - Enable system audio for narration
   - Use good microphone (not laptop built-in if possible)

### During Recording

1. **Introduction**: 
   - Face camera, introduce yourself and project
   - Speak clearly and at moderate pace

2. **Slides Section**:
   - Screen share presentation
   - Advance slides smoothly
   - Use laser pointer or annotations to highlight

3. **Live Demo**:
   - Switch to terminal + application window
   - Maximize terminal for readability (large font)
   - Position face clearly in camera frame
   - Navigate calmly, don't rush

4. **Conclusion**:
   - Return to final slide
   - Optional: show face again for closing remarks

### After Recording

1. **Edit** (if needed):
   - Trim any long pauses
   - Add title card at start
   - Add captions/subtitles (recommended for accessibility)
   - Ensure total runtime ≤ 3:00

2. **Export**:
   - Format: MP4 (H.264 codec)
   - Resolution: 1920x1080 or 1280x720
   - Bitrate: 5-10 Mbps
   - File size target: < 100MB if possible

3. **Quality Check**:
   - Watch full video
   - Verify audio is clear
   - Check that terminal text is readable
   - Ensure demo actually shows functionality

---

## Backup Plan (If Live Demo Fails)

**Option 1**: Use pre-recorded demo footage
- Record 2-3 runs beforehand
- Splice best segments together
- Narrate over recording

**Option 2**: Annotated screenshots
- Capture key moments (face detection, emotion display, stress alert)
- Create slide deck with screenshots
- Explain what would happen in live demo

**Option 3**: Flowchart walkthrough
- Show FSM state diagram
- Walk through state transitions
- Reference code snippets

---

## Timing Breakdown (Target)

| Section | Duration | Content |
|---------|----------|---------|
| Introduction | 0:30 | Problem \u0026 solution intro |
| Part I (Problem/Multimodal) | 0:45 | ARCADE framework, pros/cons |
| Part II (User/Design) | 0:45 | Persona, architecture, specs |
| Part III (Demo) | 0:45 | Live application demo |
| Conclusion | 0:15 | Summary \u0026 closing |
| **Total** | **3:00** | |

---

## Key Messages to Convey

1. **Clear Problem Definition**: Lack of early stress detection awareness
2. **Multimodal Solution**: ARCADE framework with camera, voice, touch
3. **User-Centered**: Persona-driven design (Maria)
4. **Technical Competence**: Working prototype with FSM, CNN, time-windows
5. **Ethical Awareness**: Privacy-first, acknowledges limitations
6. **Practical Implementation**: Real code, real functionality

---

## Common Questions to Anticipate

**Q: How accurate is the emotion detection?**  
A: Current demo model is untrained (random predictions). With a proper FER+ model trained on FER-2013, we'd expect 70-80% accuracy on clear frontal faces in good lighting. Real-world accuracy is lower due to individual variation and context.

**Q: What about privacy concerns?**  
A: All processing is local—no cloud uploads. Raw video frames are never stored, only emotion classifications. Users can pause anytime and data retention is limited to 30 days.

**Q: Can this replace therapy?**  
A: Absolutely not. MindCare is a self-awareness tool that might encourage seeking professional help, not a replacement for therapy.

**Q: What if there are multiple people in frame?**  
A: Current implementation detects the largest face only. Multi-person scenarios would require enhanced face tracking.

**Q: How long did this take to implement?**  
A: Approximately [X weeks/hours] for research, design, and coding. The modular architecture allows for incremental development.

---

**Good luck with your demo!**
