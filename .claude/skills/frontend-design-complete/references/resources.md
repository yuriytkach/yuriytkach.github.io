# Research, Inspiration & Learning Resources

## Common Issues Quick Reference

| Issue | Cause | Fix |
|-------|-------|-----|
| Hero left-aligned with empty space | Grid reserves hidden column | Switch to flex on mobile |
| Form fields cut off | Fixed-width grid | Stack vertically with flex |
| Inconsistent alert alignment | Missing align-items | Add `align-items: center` + `text-align: center` |
| Invisible form controls | Transparent borders | Add explicit borders or shadows |
| White text on light background | Hardcoded colors | Use semantic CSS variables |
| Horizontal scroll on selections | Too many items | Use accordion pattern |
| Textarea looks wrong | Pill border-radius | Use smaller radius for textarea |
| Design looks "AI-generated" | AI slop patterns | Run the full audit: `references/design-audit.md` (detection signals, scoring, report template) |
| Layout shift on load | Images without dimensions | Add `width`/`height` or `aspect-ratio` (Part 19) |
| Dark mode looks washed out | Colors not desaturated | Reduce saturation ~20% for dark mode (Part 20) |
| AI responses feel broken | No streaming indicator | Add typewriter cursor and phase-based loading (Part 21) |
| Specificity wars in CSS | No cascade management | Use `@layer` for explicit ordering (Part 31) |
| Content unreadable in translation | Fixed-width containers | Use logical properties and flexible layouts (Part 28) |
| Flash of wrong theme | Theme loads after paint | Run theme script in `<head>` (Part 20) |


## Part 5: Design Research & Inspiration Resources

Use these curated resources during the research phase to gather authentic inspiration, study proven patterns, and avoid generic design decisions.

### Curation & Reference Platforms

**Are.na** - https://www.are.na
Visual research tool for building mood boards and connecting ideas. Use for assembling contextual reference libraries, tracking design influences, and creating shareable channels documenting design processes. Think of it as "playlists for ideas" - following genuine curiosity leads to deeper creative engagement than algorithmic suggestions.

**Mobbin** - https://mobbin.com
UI pattern library with 1,150+ apps, 586,700+ screens, and 312,000+ user flows. Search by screens, UI elements, flows, or text within screenshots. Features apps from Airbnb, Uber, ChatGPT, Dropbox, Nike. Includes Figma plugin for direct download. Use to study how leading apps handle specific design challenges and explore complete user journeys.

**Logggos** - https://www.logggos.club
Curated logo gallery organized by business sectors (Tech, DTC, Agencies) and filterable by typography styles (sans-serif, script, serif), colors, and geometric shapes. Use when designing logo-adjacent elements or studying brand identity patterns.

### Icons & Visual Assets

**The Noun Project** - https://thenounproject.com
10M+ human-curated icons and photos in SVG/PNG formats. Emphasizes "Made by Humans" curation over algorithmic content. Use for quick icon discovery during design workflows, but consider creating custom icons for distinctive projects.

**Artvee** - https://artvee.com
High-resolution public domain paintings, posters, and illustrations. Categories include Abstract, Figurative, Landscape, Still Life, Religion, Mythology. All files freely usable for personal and commercial projects. Use for incorporating classical artwork, creating derivative works, or adding historical visual elements.

**Mockupworld** - https://www.mockupworld.co
Free photo-realistic PSD mockups for devices (iPhone, iPad, MacBook), packaging, print materials, and vehicles. Use to present designs in realistic contexts for client presentations or portfolio pieces.

### Site Builders for Reference

**Cargo** - https://cargo.site
Site builder for designers and artists with strong creative focus. Study Cargo sites for clean portfolio presentations and community-curated examples of quality design.

**Readymag** - https://readymag.com
Specialized for creating cool animations and extravagant transitions. Study Readymag projects for motion design inspiration and experimental layout approaches.

### Web Design Inspiration

**Godly.website** - https://godly.website
"Astronomically good web design inspiration" - 1,000+ curated exceptional websites spanning diverse industries. Features work from recognized design leaders (Metalab, Lusion, Notion, Stripe) and emerging talent. Use for studying cutting-edge design approaches.

**Minimal Gallery** - https://minimal.gallery
Hand-picked minimalist web design since 2013. Rigorous human curation (most submissions rejected). Organized by industry and design approach. Use for studying purposeful, clean design that prioritizes both visual elegance and usability.

**Brutalist Websites** - https://brutalistwebsites.com
Curated collection of brutalist web design with interviews. Key principles: technical honesty over polish, anti-commercial stance, content-first approach, bare-bones functionality. Features magazine sites, portfolios, and experimental platforms. Use to understand deliberate aesthetic rejection and information-first design.

**Landingfolio** - https://landingfolio.com
Landing page inspiration and templates organized by design approach and industry. Use for studying effective conversion-focused layouts and call-to-action patterns.

### Foundational Learning

**Degreeless.design** - https://degreeless.design
Comprehensive self-directed design education resource. Organized in progressive stages: Basics (typography, color theory, design history), UX Essentials (process, research, design systems), Advanced (industry content from Airbnb, Google). Key philosophy: "Process is the value you bring. Tools change & trends die."

**Google Fonts Knowledge** - https://fonts.google.com/knowledge
Typography guidance and principles from Google. Covers type design, font selection, pairing strategies, and web font implementation best practices.

### Blogs & Analysis

**Brand New** - https://www.underconsideration.com/brandnew/
Daily updates on logo, identity, and branding projects. Features before-and-after rebrand analysis with critical commentary. Categories: Reviewed (in-depth analysis), Noted (professional observations), Spotted (discovery-focused). Use to study branding decisions and understand what makes identity work succeed or fail.

### Experimental Design Tools

**Constraint Systems** - https://constraint.systems
Collection of experimental creative tools for unique layouts and constraint-based design exploration. Use for breaking out of conventional layout patterns.

**Whisk by Google Labs** - https://labs.google/whisk
Experimental image generation tool powered by Imagen 4. Enables "prompting with pictures" - upload reference images as creative prompts and mix ideas in new ways. Use for rapid visual exploration and concept iteration during early design phases.

### Design Systems to Study

**IBM Carbon** - https://carbondesignsystem.com
Enterprise design system emphasizing accessibility and consistency. Study for: responsive layout systems (breakpoints xs through 2xl), density options (condensed/normal), data visualization patterns, modular component architecture. Excellent reference for data-heavy applications.

**GitHub Primer** - https://primer.style
Comprehensive open-source design system with strong accessibility focus. Study for: detailed accessibility patterns and checklists, Octicons SVG icon system, design tokens (color, spacing, typography), component libraries for React/Rails.

**Material Design 3** - https://m3.material.io
Google's latest design system. Study for: typography scale (display, headline, title, label, body styles), cohesive color palette with semantic tokens, elevation system for visual hierarchy, CSS custom properties for dynamic theming.

---


## Part 17: Topic Reference Links

(Curation galleries, design systems, and education platforms live in Part 5 above — this part covers topic-specific tools and references not already listed there.)

### Foundational Principles
- **Laws of UX** - https://lawsofux.com - 30 psychological principles
- **Nielsen Norman Group** - https://www.nngroup.com - Usability research
- **Principles.design** - https://principles.design - Design principle collections

### Typography
- **Typescale** - https://typescale.com - Type scale generator
- **Fonts In Use** - https://fontsinuse.com - Real-world typography examples
- **Typewolf** - https://www.typewolf.com - Font recommendations

### Spacing & Layout
- **8-Point Grid** - https://spec.fm/specifics/8-pt-grid - Grid system methodology
- **Space, Grids and Layouts** - https://www.designsystems.com/space-grids-and-layouts/ - Spatial systems

### Ethical & Humane Design
- **Humane by Design** - https://humanebydesign.com - Ethical design patterns
- **Dark Patterns** - https://www.deceptive.design - Manipulative patterns to avoid
- **Microsoft Inclusive Design** - https://inclusive.microsoft.design - Designing for diversity

### Accessibility
- **The A11Y Project** - https://www.a11yproject.com - Community resources
- **WebAIM** - https://webaim.org - Testing and guidance
- **WCAG Quick Reference** - https://www.w3.org/WAI/WCAG21/quickref/ - Official standards

### More Inspiration Galleries
- **Hoverstat.es** - https://www.hoverstat.es - Interactive design
- **Really Good Emails** - https://reallygoodemails.com - Email design
- **SaaSFrame** - https://www.saasframe.io - SaaS interfaces
- **Refero** - https://refero.design - Design references

### Modern CSS
- **web.dev/blog** - https://web.dev/blog - Chrome team's CSS and performance updates
- **Modern CSS** - https://moderncss.dev - Practical modern CSS solutions
- **State of CSS** - https://stateofcss.com - Annual CSS survey and trends
- **Scroll-Driven Animations** - https://scroll-driven-animations.style - Interactive demos and examples

### Performance
- **web.dev/vitals** - https://web.dev/vitals - Core Web Vitals documentation
- **PageSpeed Insights** - https://pagespeed.web.dev - Performance testing tool

### Fluid Typography
- **Utopia** - https://utopia.fyi - Fluid type and space scale generator
- **Fluid Type Scale** - https://www.fluid-type-scale.com - Type scale calculator with clamp()

### AI Interface Design
- **AI Design Patterns** - https://ai-design-patterns.com - Patterns for AI interfaces
- **AIverse Design** - https://www.aiverse.design - AI UX pattern library

---


