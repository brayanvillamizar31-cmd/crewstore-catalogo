import Foundation
import PDFKit
import Vision
import AppKit

struct PageFeat {
    let pdfIndex: Int       // 1 or 2
    let pageIndex: Int      // 0-based in PDF
    let pageNum: Int        // 1-based in PDF
    let cHist: [Float]      // 75 bins (72 chromatic + 3 achromatic)
    let chromaHist: [Float] // 24 bins
    let chromaRatio: Float
    let bHist: [Float]      // 75 bins
    let cbSim: Float        // Low = full garment shot, High = close-up zoom
    let fprint: VNFeaturePrintObservation
    let dominantColors: [String]
    let ocrKeywords: [String]
}

func rgbToHsv(r: Float, g: Float, b: Float) -> (h: Float, s: Float, v: Float) {
    let maxC = max(r, max(g, b))
    let minC = min(r, min(g, b))
    let delta = maxC - minC
    var h: Float = 0
    if delta > 0.0001 {
        if maxC == r { h = 60 * (((g - b) / delta).truncatingRemainder(dividingBy: 6)) }
        else if maxC == g { h = 60 * (((b - r) / delta) + 2) }
        else { h = 60 * (((r - g) / delta) + 4) }
        if h < 0 { h += 360 }
    }
    let s = maxC == 0 ? 0 : (delta / maxC)
    return (h, s, maxC)
}

func histSim(_ a: [Float], _ b: [Float]) -> Float {
    var sum: Float = 0
    for i in 0..<a.count { sum += min(a[i], b[i]) }
    return sum
}

let colorNamesByBin: [Int: String] = [
    0: "Rojo", 1: "Naranja", 2: "Amarillo", 3: "Verde",
    4: "Verde Esmeralda", 5: "Azul Celeste", 6: "Azul Rey", 7: "Morado",
    8: "Rosado", 9: "Vino Tinto"
]

func detectNamedColors(cHist: [Float], chHist: [Float], chromaRatio: Float) -> [String] {
    var colorScores: [(String, Float)] = []
    let blackScore = cHist[72]
    let grayScore = cHist[73]
    let whiteScore = cHist[74]
    if whiteScore > 0.22 { colorScores.append(("Blanco", whiteScore)) }
    if blackScore > 0.22 { colorScores.append(("Negro", blackScore)) }
    if grayScore > 0.28 && whiteScore <= 0.22 && blackScore <= 0.22 { colorScores.append(("Gris", grayScore)) }
    
    if chromaRatio > 0.05 {
        // Hue bins (0..11, each 30 deg):
        // 0: Red (345..15), 1: Orange (15..45), 2: Yellow (45..75), 3: Yellow-Green (75..105),
        // 4: Green (105..135), 5: Teal (135..165), 6: Cyan/Sky (165..195), 7: Blue (195..225),
        // 8: Navy/Indigo (225..255), 9: Purple (255..285), 10: Pink/Magenta (285..315), 11: Rose/Crimson (315..345)
        let hueMap: [Int: String] = [
            0: "Rojo", 1: "Beige", 2: "Amarillo", 3: "Verde",
            4: "Verde", 5: "Verde", 6: "Azul Celeste", 7: "Azul",
            8: "Azul Oscuro", 9: "Morado", 10: "Rosado", 11: "Rojo"
        ]
        var namedMap: [String: Float] = [:]
        for h12 in 0..<12 {
            let val = (chHist[h12 * 2] + chHist[h12 * 2 + 1]) * chromaRatio
            if val > 0.06, let name = hueMap[h12] {
                namedMap[name, default: 0] += val
            }
        }
        for (k, v) in namedMap {
            colorScores.append((k, v))
        }
    }
    colorScores.sort { $0.1 > $1.1 }
    var res: [String] = []
    for (name, _) in colorScores {
        if !res.contains(name) { res.append(name) }
        if res.count >= 2 { break }
    }
    if res.isEmpty { res = ["Único"] }
    return res
}

func extractFeatures(pdfPath: String, pdfIndex: Int) -> [PageFeat] {
    let url = URL(fileURLWithPath: pdfPath)
    let doc = PDFDocument(url: url)!
    let count = doc.pageCount
    var feats: [PageFeat] = []
    print("Analyzing PDF \(pdfIndex) (\(count) pages)...")

    for pIdx in 0..<count {
        autoreleasepool {
            let page = doc.page(at: pIdx)!
            let w = 240, h = 320
            let img = page.thumbnail(of: NSSize(width: w, height: h), for: .mediaBox)
            let cgImg = img.cgImage(forProposedRect: nil, context: nil, hints: nil)!
            
            var rawData = [UInt8](repeating: 0, count: w * h * 4)
            let colorSpace = CGColorSpaceCreateDeviceRGB()
            let ctx = CGContext(data: &rawData, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w * 4, space: colorSpace, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
            ctx.draw(cgImg, in: CGRect(x: 0, y: 0, width: w, height: h))
            
            var cHist = [Float](repeating: 0, count: 75)
            var chHist = [Float](repeating: 0, count: 24)
            var bHist = [Float](repeating: 0, count: 75)
            var cCount: Float = 0, chCount: Float = 0, bCount: Float = 0
            
            for y in 0..<h {
                let ny = Float(y) / Float(h)
                for x in 0..<w {
                    let nx = Float(x) / Float(w)
                    let idx = (y * w + x) * 4
                    let r = Float(rawData[idx]) / 255.0
                    let g = Float(rawData[idx+1]) / 255.0
                    let b = Float(rawData[idx+2]) / 255.0
                    if (ny < 0.06 || ny > 0.94) && r > 0.96 && g > 0.96 && b > 0.96 { continue }
                    
                    let hsv = rgbToHsv(r: r, g: g, b: b)
                    let isAchromatic = hsv.s < 0.18 || hsv.v < 0.14
                    let bin75: Int
                    if isAchromatic {
                        let aBin = hsv.v < 0.30 ? 0 : (hsv.v < 0.60 ? 1 : 2)
                        bin75 = 72 + aBin
                    } else {
                        let hBin = min(7, Int((hsv.h + 15.0).truncatingRemainder(dividingBy: 360.0) / 45.0))
                        let sBin = min(2, Int(hsv.s * 3.0))
                        let vBin = min(2, Int(hsv.v * 3.0))
                        bin75 = hBin * 9 + sBin * 3 + vBin
                    }
                    
                    if nx >= 0.25 && nx <= 0.75 && ny >= 0.25 && ny <= 0.75 {
                        cHist[bin75] += 1
                        cCount += 1
                        if !isAchromatic {
                            let hBin12 = min(11, Int((hsv.h + 15.0).truncatingRemainder(dividingBy: 360.0) / 30.0))
                            let vBin2 = hsv.v > 0.5 ? 1 : 0
                            chHist[hBin12 * 2 + vBin2] += 1
                            chCount += 1
                        }
                    } else if nx < 0.14 || nx > 0.86 || (ny > 0.08 && ny < 0.18) || (ny > 0.82 && ny < 0.92) {
                        bHist[bin75] += 1
                        bCount += 1
                    }
                }
            }
            if cCount > 0 { for i in 0..<75 { cHist[i] /= cCount } }
            if chCount > 0 { for i in 0..<24 { chHist[i] /= chCount } }
            if bCount > 0 { for i in 0..<75 { bHist[i] /= bCount } }
            
            let cRatio = cCount > 0 ? chCount / cCount : 0
            let domColors = detectNamedColors(cHist: cHist, chHist: chHist, chromaRatio: cRatio)
            
            let cropRect = CGRect(x: Int(Double(w)*0.18), y: Int(Double(h)*0.18), width: Int(Double(w)*0.64), height: Int(Double(h)*0.64))
            let centerCg = cgImg.cropping(to: cropRect)!
            let handler = VNImageRequestHandler(cgImage: centerCg, options: [:])
            let fpReq = VNGenerateImageFeaturePrintRequest()
            let txtReq = VNRecognizeTextRequest()
            txtReq.recognitionLevel = .fast
            txtReq.usesLanguageCorrection = false
            try? handler.perform([fpReq, txtReq])
            let fp = fpReq.results!.first!
            
            var words: [String] = []
            if let obsList = txtReq.results {
                for obs in obsList {
                    if let top = obs.topCandidates(1).first {
                        let s = top.string.uppercased().trimmingCharacters(in: .whitespacesAndNewlines)
                        if s.count >= 2 { words.append(s) }
                    }
                }
            }
            
            feats.append(PageFeat(
                pdfIndex: pdfIndex,
                pageIndex: pIdx,
                pageNum: pIdx + 1,
                cHist: cHist,
                chromaHist: chHist,
                chromaRatio: cRatio,
                bHist: bHist,
                cbSim: histSim(cHist, bHist),
                fprint: fp,
                dominantColors: domColors,
                ocrKeywords: words
            ))
        }
        if (pIdx + 1) % 100 == 0 {
            print("  Processed \(pIdx + 1)/\(count) pages of PDF \(pdfIndex)")
        }
    }
    return feats
}

func sameGarment(_ a: PageFeat, _ b: PageFeat, gap: Int) -> Bool {
    let cSim = histSim(a.cHist, b.cHist)
    let bSim = histSim(a.bHist, b.bHist)
    let rawChSim = histSim(a.chromaHist, b.chromaHist)
    let chSim = (a.chromaRatio < 0.10 || b.chromaRatio < 0.10) ? max(rawChSim, 0.55) : rawChSim
    if a.chromaRatio >= 0.04 && b.chromaRatio >= 0.04 && rawChSim < 0.18 { return false }
    
    let zoomSim = max(histSim(a.cHist, b.bHist), histSim(b.cHist, a.bHist))
    var fpDist: Float = 0
    try? a.fprint.computeDistance(&fpDist, to: b.fprint)
    
    if gap == 2 {
        return bSim >= 0.72 && cSim >= 0.52 && chSim >= 0.50 && fpDist <= 0.90
    }
    
    if (zoomSim >= 0.50 || a.cbSim >= 0.40 || b.cbSim >= 0.40) && cSim >= 0.45 && chSim >= 0.40 && (bSim >= 0.44 || zoomSim >= 0.52) {
        return true
    }
    if bSim >= 0.58 && cSim >= 0.54 && chSim >= 0.48 && fpDist <= 0.96 {
        return true
    }
    if fpDist <= 0.76 && cSim >= 0.42 && chSim >= 0.42 && (bSim >= 0.45 || zoomSim >= 0.45) {
        return true
    }
    return false
}

func clusterPages(_ feats: [PageFeat]) -> [[PageFeat]] {
    var groups: [[PageFeat]] = []
    for i in 0..<feats.count {
        let cur = feats[i]
        var matchedGroup: Int? = nil
        for gIdx in stride(from: groups.count - 1, through: max(0, groups.count - 2), by: -1) {
            let g = groups[gIdx]
            if g.count >= 4 { continue }
            let gap = cur.pageNum - g.last!.pageNum
            if gap > 2 { continue }
            
            // Count how many full-frame shots (cbSim < 0.34) are already in g
            let fullCount = g.filter { $0.cbSim < 0.34 }.count
            if fullCount >= 2 && cur.cbSim < 0.34 {
                continue
            }
            
            let firstFeat = g.first!
            let lastFeat = g.last!
            if sameGarment(cur, firstFeat, gap: gap) || (gap == 1 && sameGarment(cur, lastFeat, gap: 1) && histSim(cur.cHist, firstFeat.cHist) >= 0.38) {
                matchedGroup = gIdx
                break
            }
        }
        if let gIdx = matchedGroup {
            groups[gIdx].append(cur)
        } else {
            groups.append([cur])
        }
    }
    return groups
}

let brandMap: [(pattern: String, title: String, category: String)] = [
    ("RIVER", "Camiseta River Plate Edición Especial", "Fútbol & Retro"),
    ("CABJ", "Camiseta Boca Juniors Edición Especial", "Fútbol & Retro"),
    ("BOCA", "Camiseta Boca Juniors", "Fútbol & Retro"),
    ("BARCA", "Camiseta FC Barcelona", "Fútbol & Retro"),
    ("BARCELONA", "Camiseta FC Barcelona", "Fútbol & Retro"),
    ("SPOTIFY", "Camiseta FC Barcelona", "Fútbol & Retro"),
    ("TEKA", "Camiseta Real Madrid Retro Teka", "Fútbol & Retro"),
    ("SIEMENS", "Camiseta Real Madrid Retro", "Fútbol & Retro"),
    ("EMIRATES", "Camiseta Oficial Fly Emirates", "Fútbol & Retro"),
    ("BETPLAY", "Camiseta Junior de Barranquilla", "Fútbol Colombiano"),
    ("AGUILA", "Camiseta Junior / Selección", "Fútbol Colombiano"),
    ("COLANTA", "Camiseta Fútbol Colombiano", "Fútbol Colombiano"),
    ("A.B", "Camiseta Atlético Bucaramanga", "Atlético Bucaramanga"),
    ("BUCAROS", "Camiseta Atlético Bucaramanga", "Atlético Bucaramanga"),
    ("LEONA", "Camiseta Retro Leona", "Fútbol Colombiano"),
    ("CRISTAL", "Camiseta Retro Cristal Oro", "Atlético Bucaramanga"),
    ("MAC POLLO", "Camisilla Basket Bucaramanga Mac Pollo", "Atlético Bucaramanga"),
    ("DEPORTE TOTAL", "Prenda Atlético Bucaramanga", "Atlético Bucaramanga"),
    ("FINANCIERA", "Camiseta Oficial Bucaramanga", "Atlético Bucaramanga"),
    ("RAMEDICAS", "Camiseta Oficial Bucaramanga", "Atlético Bucaramanga"),
    ("LOTTO", "Chaqueta / Prenda Deportiva Lotto", "Chaquetas & Sudaderas"),
    ("AIG", "Camiseta Manchester United Retro", "Fútbol & Retro"),
    ("PIRELLI", "Camiseta Inter de Milán Retro", "Fútbol & Retro"),
    ("ESPIRITO", "Camiseta Sporting Lisboa Retro", "Fútbol & Retro"),
    ("PISTONS", "Jersey NBA Detroit Pistons", "NBA & Basket"),
    ("RODMAN", "Jersey NBA Pistons Rodman #10", "NBA & Basket"),
    ("BULLS", "Jersey NBA Chicago Bulls", "NBA & Basket"),
    ("PIPPEN", "Jersey NBA Bulls Pippen #33", "NBA & Basket"),
    ("JORDAN", "Jersey Basket Jordan", "NBA & Basket"),
    ("LAKERS", "Jersey NBA LA Lakers", "NBA & Basket"),
    ("BRYANT", "Jersey NBA Lakers Bryant #8", "NBA & Basket"),
    ("MAGIC", "Jersey NBA Orlando Magic", "NBA & Basket"),
    ("NEAL", "Jersey NBA Magic O'Neal #32", "NBA & Basket"),
    ("UTAH", "Jersey NBA Utah Jazz", "NBA & Basket"),
    ("USA", "Jersey Selección USA", "NBA & Basket"),
    ("MEXIC", "Camiseta Selección México", "Selecciones"),
    ("CHARTERED", "Camiseta Liverpool FC", "Fútbol & Retro"),
    ("CHELSEA", "Camiseta Chelsea FC", "Fútbol & Retro"),
    ("REEBOK", "Camiseta Selección Colombia Retro", "Selecciones"),
    ("BRASIL", "Camiseta Selección Brasil", "Selecciones"),
    ("VODAFONE", "Camiseta Borussia Dortmund", "Fútbol & Retro"),
    ("JEEP", "Camiseta Juventus FC", "Fútbol & Retro"),
    ("ETIHAD", "Camiseta Manchester City", "Fútbol & Retro"),
    ("BETANO", "Camiseta Flamengo / Oficial", "Fútbol & Retro"),
    ("SANTA FE", "Camiseta Independiente Santa Fe", "Fútbol Colombiano"),
    ("BMG", "Camiseta Santos FC Brasil", "Fútbol & Retro"),
    ("DIESEL", "Camiseta Urbana Diesel", "Moda Urbana & Casual"),
    ("BOSS", "Camiseta Urbana Hugo Boss", "Moda Urbana & Casual"),
    ("LACOSTE", "Buzo / Prenda Lacoste", "Moda Urbana & Casual"),
    ("ADIDAS", "Prenda Deportiva Adidas", "Moda Deportiva"),
    ("NIKE", "Prenda Deportiva Nike", "Moda Deportiva")
]

func inferTitleAndCategory(group: [PageFeat], seqId: Int, primaryColor: String) -> (String, String) {
    let allText = group.flatMap { $0.ocrKeywords }.joined(separator: " ")
    for item in brandMap {
        if allText.contains(item.pattern) {
            return ("\(item.title) \(String(format: "%03d", seqId))", item.category)
        }
    }
    let category = group.first!.pdfIndex == 1 ? "Fútbol & Urbano" : "Camisetas & Jerseys"
    return ("Prenda CrewStore \(primaryColor) \(String(format: "%03d", seqId))", category)
}

let pdf1Path = "/Users/ginavillamizar/Downloads/crewstore catalogooo/WhatsApp Image 2026-07-22 at 11.30.16.pdf"
let pdf2Path = "/Users/ginavillamizar/Downloads/crewstore catalogooo/WhatsApp Image 2026-08-20 at 14.57.50.pdf"
let outDir = "/Users/ginavillamizar/Documents/crewstore-catalogo/products"

let feats1 = extractFeatures(pdfPath: pdf1Path, pdfIndex: 1)
let groups1 = clusterPages(feats1)
print("PDF 1 clustered into \(groups1.count) products.")

let feats2 = extractFeatures(pdfPath: pdf2Path, pdfIndex: 2)
let groups2 = clusterPages(feats2)
print("PDF 2 clustered into \(groups2.count) products.")

let allGroups = groups1 + groups2
print("Total grouped products: \(allGroups.count). Rendering optimized images...")

let doc1 = PDFDocument(url: URL(fileURLWithPath: pdf1Path))!
let doc2 = PDFDocument(url: URL(fileURLWithPath: pdf2Path))!

func savePageJpg(doc: PDFDocument, pageIndex: Int, outPath: String) {
    autoreleasepool {
        let page = doc.page(at: pageIndex)!
        let img = page.thumbnail(of: NSSize(width: 960, height: 1280), for: .mediaBox)
        if let tiff = img.tiffRepresentation,
           let rep = NSBitmapImageRep(data: tiff),
           let jpg = rep.representation(using: .jpeg, properties: [.compressionFactor: 0.82]) {
            try? jpg.write(to: URL(fileURLWithPath: outPath), options: .atomic)
        }
    }
}

var catalogJSON: [[String: Any]] = []

for (idx, g) in allGroups.enumerated() {
    let prodId = idx + 1
    let code = String(format: "REF-%03d", prodId)
    
    // Sort pages in group so the best full-garment shot is first
    let sortedPages = g.sorted { a, b in
        let scoreA = a.cbSim + Float(a.pageNum - g[0].pageNum) * 0.03
        let scoreB = b.cbSim + Float(b.pageNum - g[0].pageNum) * 0.03
        return scoreA < scoreB
    }
    
    let primaryFeat = sortedPages[0]
    let doc = primaryFeat.pdfIndex == 1 ? doc1 : doc2
    
    var imagePaths: [String] = []
    for (mIdx, feat) in sortedPages.enumerated() {
        let relPath = mIdx == 0 ? "products/item_\(prodId).jpg" : "products/item_\(prodId)_\(mIdx + 1).jpg"
        let fullOut = "/Users/ginavillamizar/Documents/crewstore-catalogo/\(relPath)"
        savePageJpg(doc: doc, pageIndex: feat.pageIndex, outPath: fullOut)
        imagePaths.append(relPath)
    }
    
    let colors = primaryFeat.dominantColors
    let (title, category) = inferTitleAndCategory(group: g, seqId: prodId, primaryColor: colors.first ?? "")
    let editorialImg: Any = imagePaths.count > 1 ? imagePaths[1] : NSNull()
    
    let itemDict: [String: Any] = [
        "id": prodId,
        "code": code,
        "name": title,
        "supplierPrice": 45000,
        "marginPercent": 45,
        "manualPrice": NSNull(),
        "salePrice": 65000,
        "category": category,
        "colors": colors,
        "sizes": ["S", "M", "L", "XL"],
        "image": imagePaths[0],
        "editorialImage": editorialImg,
        "images": imagePaths,
        "inStock": true,
        "active": true,
        "description": "Prenda deportiva y urbana de alta calidad disponible en crewstore.co."
    ]
    catalogJSON.append(itemDict)
    
    if prodId % 50 == 0 || prodId == allGroups.count {
        print("  Saved product \(prodId)/\(allGroups.count)")
    }
}

let jsonData = try! JSONSerialization.data(withJSONObject: catalogJSON, options: [.prettyPrinted, .sortedKeys])
try! jsonData.write(to: URL(fileURLWithPath: "/Users/ginavillamizar/Documents/crewstore-catalogo/products.json"))

var jsStr = "window.CATALOG_PRODUCTS = " + String(data: jsonData, encoding: .utf8)! + ";\n"
try! jsStr.write(toFile: "/Users/ginavillamizar/Documents/crewstore-catalogo/products.js", atomically: true, encoding: .utf8)

print("Done! Generated \(catalogJSON.count) products in /Users/ginavillamizar/Documents/crewstore-catalogo/products.json")
