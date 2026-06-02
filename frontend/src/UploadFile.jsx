function UploadFile() {
    return (
        <section className="mb-stack-lg">
            <div className="file-drop-zone rounded-xl bg-surface-container-low p-stack-lg flex flex-col items-center justify-center border-2 border-transparent transition-all duration-300 group cursor-pointer hover:bg-on-tertiary-container/10" id="drop-zone">
                <div className="w-16 h-16 rounded-full bg-primary-container/10 flex items-center justify-center text-primary mb-4 group-hover:scale-110 transition-transform">
                <span className="material-symbols-outlined text-[32px]">upload_file</span>
                </div>
                <h2 className="font-headline-md text-on-surface mb-1">Drag and drop files to upload</h2>
                <p className="text-on-surface-variant text-body-md mb-6">Support for images, videos, and PDF documents up to 500MB</p>
                <button className="bg-primary text-on-primary px-8 py-3 rounded-lg font-button flex items-center gap-2 shadow-sm hover:brightness-110 active:scale-95 transition-all">
                Browse Files
                </button>
            </div>
        </section>
    )
}

export default UploadFile