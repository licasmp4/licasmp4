import Cocoa
import WebKit
// uso: quadros <url-da-pagina> <pasta-saida>  → grava q000.png… chamando window.quadro(i)
let args = CommandLine.arguments
let app = NSApplication.shared
app.setActivationPolicy(.accessory)
class D: NSObject, WKNavigationDelegate {
  let wv = WKWebView(frame: NSRect(x: 0, y: 0, width: 1300, height: 700))
  var pasta = ""; var n = 0; var i = 0
  func webView(_ w: WKWebView, didFinish nav: WKNavigation!) {
    w.evaluateJavaScript("window.N") { v, e in
      if let e = e { print("erro N:", e); exit(1) }
      self.n = (v as? Int) ?? 0; print("quadros:", self.n); self.proximo()
    }
  }
  func proximo() {
    if i >= n { exit(0) }
    wv.evaluateJavaScript("window.quadro(\(i))") { v, e in
      if let e = e { print("erro quadro \(self.i):", e); exit(1) }
      let s = (v as! String).components(separatedBy: ",")[1]
      try! Data(base64Encoded: s)!.write(to: URL(fileURLWithPath: String(format: "%@/q%03d.png", self.pasta, self.i)))
      self.i += 1; self.proximo()
    }
  }
}
let d = D(); d.pasta = args[2]
let win = NSWindow(contentRect: d.wv.frame, styleMask: [.borderless], backing: .buffered, defer: false)
win.contentView = d.wv; win.setFrameOrigin(NSPoint(x: -5000, y: 0)); win.orderFront(nil)
d.wv.navigationDelegate = d
let url = URL(string: args[1])!
d.wv.loadFileURL(url, allowingReadAccessTo: URL(fileURLWithPath: "/tmp/claude-501/lp"))
DispatchQueue.main.asyncAfter(deadline: .now() + 300) { print("tempo esgotado"); exit(2) }
app.run()
