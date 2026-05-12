import subprocess
import os
import platform

def export_html_to_pdf(html_path, pdf_path):
    """
    Exports an HTML file to PDF using Microsoft Edge headless mode on Windows.
    """
    print(f"[*] Exporting {html_path} to PDF...")
    
    # Ensure absolute paths
    abs_html_path = os.path.abspath(html_path)
    abs_pdf_path = os.path.abspath(pdf_path)
    
    # Convert path to file URI for Edge
    file_uri = f"file:///{abs_html_path.replace('\\', '/')}"
    
    if platform.system() == "Windows":
        edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        if not os.path.exists(edge_path):
            print("[!] Microsoft Edge not found at default location. Cannot export PDF.")
            return False
            
        cmd = [
            edge_path,
            "--headless",
            "--disable-gpu",
            "--run-all-compositor-stages-before-draw",
            "--print-to-pdf-no-header",
            f"--print-to-pdf={abs_pdf_path}",
            file_uri
        ]
        
        try:
            # Run the command
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"[+] PDF successfully exported to: {abs_pdf_path}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"[!] Error exporting PDF: {e}")
            print(e.stderr)
            return False
    else:
        print("[!] Automatic PDF export is currently only supported on Windows using Edge.")
        return False
