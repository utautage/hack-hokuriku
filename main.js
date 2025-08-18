test();

async function test() {
    // const response = await fetch("https://raw.githubusercontent.com/hokuriku-inbound-kanko/mac-address/refs/heads/main/00_M5_facility%20list.csv");
    // const text = await response.text();
    // let lines = text.split("\n");
    // lines = lines.filter((line) => !/^\,*$/.test(line));
    // for (let i = 0; i < lines.length; i++) {
    //     lines[i] = lines[i].split(",");
    // }    
    // const table = document.createElement("table");
    // const thead = document.createElement("thead");
    // const tbody = document.createElement("tbody");
    
    // // ヘッダー行を生成
    // const headerRow = document.createElement("tr");
    // Object.keys(lines[0]).forEach((key) => {
    //     const th = document.createElement("th");
    //     th.textContent = key;
    //     headerRow.appendChild(th);
    // });
    // thead.appendChild(headerRow);
    
    // // データ行を生成
    // lines.forEach((row) => {
    //     const tr = document.createElement("tr");
    //     Object.values(row).forEach((value) => {
    //         const td = document.createElement("td");
    //         td.textContent = value;
    //         tr.appendChild(td);
    //     });
    //     tbody.appendChild(tr);
    // });
    
    // table.appendChild(thead);
    // table.appendChild(tbody);
    // document.getElementById("output").appendChild(table);
}
