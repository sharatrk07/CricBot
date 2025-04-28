// Table.jsx
import React from "react"

const KEY_RENAMES = {
  "4s": "Fours",
  "6s": "Sixes",
  BF: "Balls Faced",
  Inns: "Innings",
  Mins: "Minutes",
  Pos: "Position",
  SR: "Strike Rate",
  "Start Date": "Match Date",
  Ave: "Average",
  HS: "Highest Score",
  Mat: "Matches",
  NO: "Not Out",
  "Bat Av": "Batting Average",
  Ct: "Catches",
  St: "Stumpings",
  LS: "Least Score",
  NR: "Not Result",
  RPO: "Runs Per Over",
  Econ: "Economy",
  Wkts: "Wickets",
  Wkt: "Wickets",
  BBI: "Best Bowling",
  5: "5 Wickets",
  Conc: "Conceeded",
  Ex: "Extras",
  Mdns: "Maidens",
  4: "4 Wickets",
}

function Table({ data, filtersData, index, total }) {
  if (!data || typeof data !== "object" || Object.keys(data).length === 0)
    return null

  const flat = { ...data }
  if (flat.Details && typeof flat.Details === "object") {
    Object.entries(flat.Details).forEach(([k, v]) => {
      flat[k.trim()] = v
    })
    delete flat.Details
  }
  delete flat.IconPath

  let specialKey = null,
    specialValue = null
  if (flat.Units != null && flat.Value != null) {
    if (![0, "0", "-"].includes(flat.Value)) {
      specialKey = flat.Units
      specialValue = flat.Value
    }
    delete flat.Units
    delete flat.Value
  }

  let name = ""
  if (flat.Name) {
    name = typeof flat.Name === "object" && flat.Name.Name ? flat.Name.Name : flat.Name
    delete flat.Name
  }
  if (!name && filtersData) {
    const first = filtersData.split(",")[0]
    if (first.includes(":")) name = first.split(":")[1].trim()
  }

  if (total === 5) {
    name = `${index + 1}. ${name}`
  }

  let rows = Object.entries(flat).filter(
    ([k, v]) =>
      !["0", "subText"].includes(k) &&
      typeof v !== "object" &&
      v !== 0 &&
      v !== "0" &&
      v !== "-"
  )

  const numeric = [],
    strings = []
  rows.forEach(([k, v]) => {
    const num = Number.parseFloat(v)
    if (!isNaN(num)) numeric.push([k, v])
    else strings.push([k, v])
  })
  numeric.sort((a, b) => Number.parseFloat(b[1]) - Number.parseFloat(a[1]))
  rows = [...numeric, ...strings]

  return (
    <div className="w-full my-4 bg-gray-800 rounded-lg overflow-hidden shadow-lg border border-gray-700">
      <h2 className="text-sm font-bold text-white p-3 bg-gray-700 border-b border-gray-600">
        {name}
      </h2>
      <div className="overflow-x-auto">
        <table className="table-auto text-xs w-full">
          <tbody>
            {specialKey && (
              <tr>
                <td
                  style={{ width: "150px" }}
                  className="py-2 px-4 font-semibold text-gray-300 text-sm border-b border-gray-700 bg-gray-750"
                >
                  {KEY_RENAMES[specialKey] || specialKey}
                </td>
                <td
                  style={{ width: "200px" }}
                  className="py-2 px-4 font-semibold text-gray-300 text-sm border-b border-gray-700 bg-gray-750"
                >
                  {specialValue}
                </td>
              </tr>
            )}
            {rows.map(([key, value], idx) => (
              <tr
                key={idx}
                className={idx % 2 === 0 ? "bg-gray-800" : "bg-gray-750 hover:bg-gray-700"}
              >
                <td
                  style={{ width: "150px" }}
                  className="py-2 px-4 border-b border-gray-700 font-medium text-gray-300"
                >
                  {KEY_RENAMES[key] || key}
                </td>
                <td
                  style={{ width: "200px" }}
                  className="py-2 px-4 border-b border-gray-700 text-white"
                >
                  {value}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Table


















// WORKING PERFECTLY
// // Table.jsx
// import React from "react";

// const KEY_RENAMES = {
//   "4s": "Fours",
//   "6s": "Sixes",
//   BF: "Balls Faced",
//   Inns: "Innings",
//   Mins: "Minutes",
//   Pos: "Position",
//   SR: "Strike Rate",
//   "Start Date": "Match Date",
//   Ave: "Average",
//   HS: "Highest Score",
//   Mat: "Matches",
//   NO: "Not Out",
//   "Bat Av": "Batting Average",
//   Ct: "Catches",
//   St: "Stumpings",
//   LS: "Least Score",
//   NR: "Not Result",
//   RPO: "Runs Per Over",
// };

// function Table({ data, filtersData, index, total }) {
//   if (!data || typeof data !== "object" || Object.keys(data).length === 0)
//     return null;

//   const flat = { ...data };
//   if (flat.Details && typeof flat.Details === "object") {
//     Object.entries(flat.Details).forEach(([k, v]) => {
//       flat[k.trim()] = v;
//     });
//     delete flat.Details;
//   }
//   delete flat.IconPath;

//   let specialKey = null, specialValue = null;
//   if (flat.Units != null && flat.Value != null) {
//     if (![0, "0", "-"].includes(flat.Value)) {
//       specialKey = flat.Units;
//       specialValue = flat.Value;
//     }
//     delete flat.Units;
//     delete flat.Value;
//   }

//   let name = "";
//   if (flat.Name) {
//     name = typeof flat.Name === "object" && flat.Name.Name
//       ? flat.Name.Name
//       : flat.Name;
//     delete flat.Name;
//   }
//   if (!name && filtersData) {
//     const first = filtersData.split(",")[0];
//     if (first.includes(":")) name = first.split(":")[1].trim();
//   }

//   if (total === 5) {
//     name = `${index + 1}. ${name}`;
//   }

//   let rows = Object.entries(flat).filter(
//     ([k, v]) =>
//       !["0", "subText"].includes(k) &&
//       typeof v !== "object" &&
//       v !== 0 &&
//       v !== "0" &&
//       v !== "-"
//   );

//   const numeric = [], strings = [];
//   rows.forEach(([k, v]) => {
//     const num = parseFloat(v);
//     if (!isNaN(num)) numeric.push([k, v]);
//     else strings.push([k, v]);
//   });
//   numeric.sort((a, b) => parseFloat(b[1]) - parseFloat(a[1]));
//   rows = [...numeric, ...strings];

//   return (
//     <div className="ml-4 my-2 max-w-max bg-gray-800 rounded-lg overflow-hidden">
//       <h2 className="text-sm font-bold text-white p-1 bg-gray-700">{name}</h2>
//       <div className="overflow-x-auto">
//         <table className="table-auto text-xs">
//           <tbody>
//             {specialKey && (
//               <tr>
//                 <td
//                   style={{ width: "150px" }}
//                   className="py-0.5 px-1 font-semibold text-blue-400 text-sm border-b border-gray-700"
//                 >
//                   {KEY_RENAMES[specialKey] || specialKey}
//                 </td>
//                 <td
//                   style={{ width: "200px" }}
//                   className="py-0.5 px-1 font-semibold text-blue-400 text-sm border-b border-gray-700"
//                 >
//                   {specialValue}
//                 </td>
//               </tr>
//             )}
//             {rows.map(([key, value], idx) => (
//               <tr
//                 key={idx}
//                 className={idx % 2 === 0 ? "bg-gray-800" : "bg-gray-750"}
//               >
//                 <td
//                   style={{ width: "150px" }}
//                   className="py-0.5 px-1 border-b border-gray-700 font-medium text-gray-300"
//                 >
//                   {KEY_RENAMES[key] || key}
//                 </td>
//                 <td
//                   style={{ width: "200px" }}
//                   className="py-0.5 px-1 border-b border-gray-700 text-white"
//                 >
//                   {value}
//                 </td>
//               </tr>
//             ))}
//           </tbody>
//         </table>
//       </div>
//     </div>
//   );
// }

// export default Table;