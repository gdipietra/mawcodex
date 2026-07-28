# Teaching project deployment profile

Use this profile in addition to the core JAW workflow when teaching artifacts
are material.

## Course identity

- Identify institution, course, level, audience, prerequisites, term, and
  working language. Do not assume English; record PT-BR or bilingual output
  explicitly.
- Map the curriculum arc, notation registry, recurring examples, and the
  relationship between lecture notes, slides, exercises, and assessments.
- Preserve established preambles, themes, branding, and accessibility rules.

## Content authority and protected material

- Identify the source of truth for Beamer, Quarto, notebooks, PDFs, or an LMS.
- Distinguish instructor sources from generated student-facing outputs.
- Separate exercises from solutions and exams from answer keys. Treat hidden
  solutions, future assessments, grades, and student data as protected.
- Record copyright and license roles for textbooks, papers, figures, problem
  banks, and imported media.

## Build readiness

- Test the actual TeX engine and bibliography path used by a representative
  deck or handout.
- Render the actual Quarto target if Quarto is present.
- Run representative code or notebooks that generate course figures or
  examples.
- Inspect a rendered page or slide for fonts, language, equations, clipping,
  and asset resolution.
- Confirm generated artifacts and caches stay out of the source tree or are
  intentionally tracked.

## Minimum teaching readiness evidence

| Area | Evidence |
| --- | --- |
| Course | audience, language, prerequisites, curriculum position |
| Sources | authority for notes, slides, lists, exams, and mirrors |
| Protection | solution keys, exams, student data, copyrighted inputs |
| LaTeX | representative compile with required engine and bibliography |
| Quarto | representative render when used |
| Computation | figure/notebook entry points and runtimes |
| Pedagogy | notation, accessibility, examples, and review conventions |
| Publication | LMS/web/Overleaf authority and responsible approver |
