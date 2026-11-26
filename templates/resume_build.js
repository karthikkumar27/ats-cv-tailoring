// ATS-safe resume builder. Optional: use it when you want the exact same layout every time.
// Copy it to profile/resume_build.js, replace the invented data in `cv`, then:
//   npm install docx@9   (tested with 9.5.1)
//   node profile/resume_build.js applications/<Company>_<Role>/<First>_<Last>_<Role>_<Company>.docx
// Layout follows the format rules in SKILL.md: one column, no tables or text boxes,
// contact details in the body, Calibri 10pt, A4, standard headings, plain bullets.
// Colour is only on the headline and links: ATS parsers ignore colour, recruiters see it.

const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, ExternalHyperlink, BorderStyle, LevelFormat, AlignmentType } = require("docx");

// Everything below is invented. Maya Tan is not a real person.
const cv = {
  name: "Maya Tan",
  headline: "Senior Backend Engineer | Python, Go, PostgreSQL, AWS",
  // Each contact line is a list of parts; parts with a `link` become clickable.
  contact: [
    ["Singapore", "+65 8000 0000", { text: "maya.tan@example.com", link: "mailto:maya.tan@example.com" }],
    [
      { text: "linkedin.com/in/example", link: "https://linkedin.com/in/example" },
      { text: "github.com/example", link: "https://github.com/example" },
    ],
  ],
  availability: "1 month notice",
  summary:
    "Backend engineer with 6 years building Python and Go services for billing and logistics. " +
    "Moved 2 million invoices to PostgreSQL with no reconciliation errors, and cut p95 API latency by 40%. " +
    "Mentored 4 junior engineers.",
  skills: [
    ["Languages", "Python, Go"],
    ["Databases", "PostgreSQL (query tuning, indexing)"],
    ["Cloud", "AWS (Lambda, SQS, RDS)"],
  ],
  experience: [
    {
      title: "Senior Backend Engineer",
      company: "Northwind Logistics",
      location: "Singapore",
      dates: "Mar 2022 – Present",
      bullets: [
        "Moved the billing system from MySQL to PostgreSQL, 2 million invoices with no reconciliation errors.",
        "Cut p95 API latency by 40% by rewriting the slowest PostgreSQL queries and adding covering indexes.",
        "Built an order events pipeline on AWS Lambda and SQS that handles 300,000 messages a day.",
        "Mentored 4 junior engineers through code review and weekly pairing.",
      ],
      projects: null, // optional "Selected projects:" line under the bullets
    },
    {
      title: "Backend Engineer",
      company: "Bluebird Retail",
      location: "Kuala Lumpur, Malaysia",
      dates: "Jun 2020 – Feb 2022",
      bullets: [
        "Wrote Go services for stock reservations across 120 stores.",
        "Moved nightly reports from cron scripts to scheduled Lambda jobs, saving an estimated 10 hours of manual work a week.",
      ],
    },
  ],
  projects: [
    {
      name: "invoice-diff: Invoice Reconciliation CLI",
      type: "Open-source project", // or "Personal project"
      link: { text: "github.com/example/invoice-diff", url: "https://github.com/example/invoice-diff" }, // optional
      bullets: ["Built a Python CLI that compares invoice exports between two databases and reports mismatches."],
    },
  ],
  education: [
    { degree: "BSc Computer Science", school: "Example University", location: "Singapore", dates: "2016 – 2020" },
  ],
  certifications: ["AWS Certified Developer – Associate (Amazon Web Services, 2024)"], // leave [] for none
  extra: [],
};

const FONT = "Calibri";
const BODY = 20; // half-points, so 20 = 10pt
const BLUE = "1F4E79"; // headline and links

const run = (text, opts = {}) => new TextRun({ text, font: FONT, size: BODY, ...opts });
const link = (url, label) => new ExternalHyperlink({ link: url, children: [run(label, { color: BLUE })] });
const para = (children, opts = {}) =>
  new Paragraph({ spacing: { after: 55 }, ...opts, children: Array.isArray(children) ? children : [children] });
const heading = (text) =>
  new Paragraph({
    spacing: { before: 125, after: 45 },
    keepNext: true,
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "808080", space: 2 } },
    children: [run(text.toUpperCase(), { bold: true, size: 22 })],
  });
const bullet = (text) => new Paragraph({ numbering: { reference: "b", level: 0 }, spacing: { after: 35 }, children: [run(text)] });
function job(title, company, location, dates, bullets, projects) {
  return [
    new Paragraph({ spacing: { before: 85, after: 0 }, keepNext: true, children: [run(title, { bold: true, size: 21 })] }),
    new Paragraph({ spacing: { after: 45 }, keepNext: true, children: [run(`${company} | ${location} | ${dates}`, { italics: true })] }),
    ...bullets.map(bullet),
    ...(projects ? [para([run("Selected projects: ", { bold: true }), run(projects)], { spacing: { before: 15, after: 20 } })] : []),
  ];
}

const children = [
  para(run(cv.name.toUpperCase(), { bold: true, size: 34 }), { spacing: { after: 20 } }),
  para(run(cv.headline, { bold: true, size: 23, color: BLUE })),
  ...cv.contact.map((line) =>
    para(
      line.flatMap((part, i) => [
        ...(i ? [run(" | ")] : []),
        typeof part === "string"
          ? run(part)
          : link(part.link, part.text),
      ]),
      { spacing: { after: 0 } }
    )
  ),
  ...(cv.availability ? [para([run("Availability: ", { bold: true }), run(cv.availability)])] : []),

  heading("Summary"),
  para(run(cv.summary)),

  heading("Skills"),
  ...cv.skills.map(([cat, items]) => para([run(`${cat}: `, { bold: true }), run(items)])),

  heading("Work Experience"),
  ...cv.experience.flatMap((j) => job(j.title, j.company, j.location, j.dates, j.bullets, j.projects)),
];

if (cv.projects.length) {
  children.push(
    heading("Projects"),
    ...cv.projects.flatMap((p) => [
      new Paragraph({ spacing: { before: 55, after: 15 }, keepNext: true, children: [run(p.name, { bold: true, size: 21 })] }),
      new Paragraph({
        spacing: { after: 45 },
        keepNext: true,
        children: [run(p.link ? `${p.type} | ` : p.type, { italics: true }), ...(p.link ? [link(p.link.url, p.link.text)] : [])],
      }),
      ...p.bullets.map(bullet),
    ])
  );
}

children.push(
  heading(cv.certifications.length ? "Education and Certifications" : "Education"),
  ...cv.education.map((e) =>
    para([run(e.degree, { bold: true }), run(` | ${e.school} | ${e.location} | ${e.dates}`)], { spacing: { after: 35 } })
  ),
  ...(cv.certifications.length ? [para([run("Certifications: ", { bold: true }), run(cv.certifications.join("; "))])] : []),
  ...cv.extra.map((line) => para(run(line), { spacing: { before: 120 } }))
);

const doc = new Document({
  creator: cv.name,
  title: `${cv.name} Resume`,
  styles: { default: { document: { run: { font: FONT, size: BODY } } } },
  numbering: {
    config: [
      {
        reference: "b",
        levels: [
          {
            level: 0,
            format: LevelFormat.BULLET,
            text: "•",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 330, hanging: 220 } } },
          },
        ],
      },
    ],
  },
  sections: [
    {
      properties: {
        // A4 in twips. For US Letter use width 12240, height 15840.
        page: { size: { width: 11906, height: 16838 }, margin: { top: 700, bottom: 700, left: 880, right: 880 } },
      },
      children,
    },
  ],
});

const out = process.argv[2] || "resume.docx";
Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(out, buf);
  console.log(`Wrote ${out}`);
});
