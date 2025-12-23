import { assembleVegaChart } from "../src/app/utils";
import { FieldItem } from "../src/components/ComponentType";

// Simple Node-based check for Top-K behavior in assembleVegaChart.
// Run with: npx ts-node perf_tests/vega_topk_check.ts

function buildHighCardinalityTable(rows: number, categories: number) {
    const table: any[] = [];
    for (let i = 0; i < rows; i++) {
        table.push({
            category: `cat_${i % categories}`,
            value: i,
        });
    }
    return table;
}

function main() {
    const workingTable = buildHighCardinalityTable(10000, 500); // 500 distinct categories

    const conceptShelfItems: FieldItem[] = [
        {
            id: "original--t--category",
            name: "category",
            source: "original",
            tableRef: "t",
        },
        {
            id: "original--t--value",
            name: "value",
            source: "original",
            tableRef: "t",
        },
    ];

    const tableMetadata: any = {
        category: { type: "string", semanticType: "", levels: [] },
        value: { type: "number", semanticType: "", levels: [] },
    };

    const encodingMap: any = {
        x: { fieldID: "original--t--category" },
        y: { fieldID: "original--t--value", aggregate: "sum" },
        color: {},
        column: {},
        row: {},
        xOffset: {},
        radius: {},
        size: {},
    };

    const [chartType, spec] = assembleVegaChart(
        "Bar Chart",
        encodingMap,
        conceptShelfItems,
        workingTable,
        tableMetadata,
        30,
        false,
        300,
        200,
        false
    ) as any;

    console.log("=== Vega Top-K check ===");
    console.log("chartType:", chartType);

    if (!spec || !spec.encoding || !spec.encoding.x || !spec.encoding.x.scale) {
        console.log("Missing x encoding or scale, cannot check domain.");
        return;
    }

    const scale = spec.encoding.x.scale;
    const domain: string[] = scale.domain;
    if (!domain || !Array.isArray(domain)) {
        console.log("No explicit domain on x scale, nothing to check.");
        return;
    }

    console.log("domain length:", domain.length);
    const placeholder = domain[domain.length - 1];
    console.log("last domain entry (placeholder):", placeholder);

    if (domain.length > 60) {
        console.log("WARNING: domain length seems too large for Top-K (>", 60, ")");
    } else {
        console.log("OK: domain length is bounded, Top-K likely effective.");
    }
}

main();
