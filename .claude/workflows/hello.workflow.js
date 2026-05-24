export const meta = {
  name: "hello",
  description: "Smallest possible workflow — prove the substrate works",
  phases: [{ title: "Greet" }]
};

const A = typeof args === "string" ? JSON.parse(args) : args || {};

phase("Greet");
const result = await agent(
  `Say hello to ${A.name || "world"} in one short sentence. Return { greeting: "<sentence>" }.`,
  {
    label: "greet",
    phase: "Greet",
    schema: {
      type: "object",
      required: ["greeting"],
      properties: { greeting: { type: "string" } }
    }
  }
);

return { greeting: result?.greeting ?? "no greeting received" };
