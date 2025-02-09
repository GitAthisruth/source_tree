import { readFileSync, writeFileSync } from "fs";
import { basename } from "path";
import { parseModule } from "esprima";



export function getImports(rawData) {
    const jsonData = JSON.parse(rawData);
    console.log("jsonData",jsonData)
    let fileImports = [];

    jsonData.file_path.forEach(filePath => {
        console.log(`Processing File: ${filePath}`);

        try {
            const fileContent = readFileSync(filePath, "utf-8");
            console.log("File Content:", fileContent);
            const fileName = basename(filePath,".js");
            console.log("File Name:", fileName);
            const ast = parseModule(fileContent, { sourceType: "module" });
            let imports = ast.body
                .filter(node => node.type === "ImportDeclaration")
                .map(node => {
                    let importName = node.source.value;
                    if (importName.startsWith("./")) {
                        importName = importName.substring(2);
                    }
                    if (importName.endsWith(".js")) {
                        importName = importName.slice(0, -3);
                    }

                    return importName;
                });

            if (imports.length > 0) {
                fileImports.push({
                    file_name: fileName,
                    imports: imports
                });
            }
        } catch (error) {
            console.error(`Error parsing ${filePath}:`, error);
        }
    });

    return fileImports;
}

const filePath = "C:\\Users\\LENOVO\\Desktop\\prizmora\\source_tree\\finding_ast_for_javascript\\all_file_paths.json";
const rawData = readFileSync(filePath, "utf-8");

const extractedImports = getImports(rawData);  

writeFileSync("import_file.json", JSON.stringify(extractedImports, null, 4), "utf-8");

console.log("Extracted imports saved to import_file.json");