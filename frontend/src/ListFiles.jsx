function ListFiles() {
    return (
        <section className="bg-surface-container-lowest rounded-xl border border-outline-variant overflow-hidden shadow-sm">
            <div className="px-6 py-4 border-b border-outline-variant flex justify-between items-center bg-surface-container-lowest">
                <h3 className="font-headline-md text-on-surface">Recent Files</h3>
                <div className="flex items-center gap-2">
                    <button className="p-2 text-on-surface-variant hover:bg-surface-container-low rounded-lg transition-colors">
                        <span className="material-symbols-outlined">filter_list</span>
                    </button>
                    <button className="p-2 text-on-surface-variant hover:bg-surface-container-low rounded-lg transition-colors">
                        <span className="material-symbols-outlined">grid_view</span>
                    </button>
                </div>
            </div>
            <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="bg-surface-container-low/30">
                            <th className="px-6 py-4 font-button text-xs text-on-surface-variant uppercase tracking-wider">Name</th>
                            <th className="px-6 py-4 font-button text-xs text-on-surface-variant uppercase tracking-wider">Date Modified</th>
                            <th className="px-6 py-4 font-button text-xs text-on-surface-variant uppercase tracking-wider">Size</th>
                            <th className="px-6 py-4 font-button text-xs text-on-surface-variant uppercase tracking-wider text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-outline-variant">

                        <tr className="hover:bg-surface-container-low transition-colors group">
                            <td className="px-6 py-4">
                                <div className="flex items-center gap-3">
                                    <div className="w-10 h-10 rounded flex items-center justify-center bg-error-container/20 text-error">
                                        <span className="material-symbols-outlined">picture_as_pdf</span>
                                    </div>
                                    <span className="font-body-md text-on-surface font-medium">Q4_Report_2023.pdf</span>
                                </div>
                            </td>
                            <td className="px-6 py-4 text-on-surface-variant text-body-md">Oct 12, 2023</td>
                            <td className="px-6 py-4 text-on-surface-variant text-body-md">2.4 MB</td>
                            <td className="px-6 py-4 text-right">
                                <div className="flex justify-end gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                                    <button className="p-2 text-on-surface-variant hover:text-primary transition-colors"><span className="material-symbols-outlined text-[20px]">download</span></button>
                                    <button className="p-2 text-on-surface-variant hover:text-error transition-colors"><span className="material-symbols-outlined text-[20px]">delete</span></button>
                                    <button className="p-2 text-on-surface-variant hover:bg-surface-container-high transition-colors rounded-full"><span className="material-symbols-outlined text-[20px]">more_vert</span></button>
                                </div>
                            </td>
                        </tr>

                        <tr className="hover:bg-surface-container-low transition-colors group">
                            <td className="px-6 py-4">
                                <div className="flex items-center gap-3">
                                    <div className="w-10 h-10 rounded flex items-center justify-center bg-primary-container/10 text-primary">
                                        <span className="material-symbols-outlined">image</span>
                                    </div>
                                    <span className="font-body-md text-on-surface font-medium">Hero_Banner_Draft.png</span>
                                </div>
                            </td>
                            <td className="px-6 py-4 text-on-surface-variant text-body-md">Oct 10, 2023</td>
                            <td className="px-6 py-4 text-on-surface-variant text-body-md">5.1 MB</td>
                            <td className="px-6 py-4 text-right">
                                <div className="flex justify-end gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                                    <button className="p-2 text-on-surface-variant hover:text-primary transition-colors"><span className="material-symbols-outlined text-[20px]">download</span></button>
                                    <button className="p-2 text-on-surface-variant hover:text-error transition-colors"><span className="material-symbols-outlined text-[20px]">delete</span></button>
                                    <button className="p-2 text-on-surface-variant hover:bg-surface-container-high transition-colors rounded-full"><span className="material-symbols-outlined text-[20px]">more_vert</span></button>
                                </div>
                            </td>
                        </tr>

                        <tr className="hover:bg-surface-container-low transition-colors group">
                            <td className="px-6 py-4">
                                <div className="flex items-center gap-3">
                                    <div className="w-10 h-10 rounded flex items-center justify-center bg-tertiary-container/10 text-tertiary">
                                        <span className="material-symbols-outlined">videocam</span>
                                    </div>
                                    <span className="font-body-md text-on-surface font-medium">Product_Demo_v2.mp4</span>
                                </div>
                            </td>
                            <td className="px-6 py-4 text-on-surface-variant text-body-md">Oct 08, 2023</td>
                            <td className="px-6 py-4 text-on-surface-variant text-body-md">124.8 MB</td>
                            <td className="px-6 py-4 text-right">
                                <div className="flex justify-end gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                                    <button className="p-2 text-on-surface-variant hover:text-primary transition-colors"><span className="material-symbols-outlined text-[20px]">download</span></button>
                                    <button className="p-2 text-on-surface-variant hover:text-error transition-colors"><span className="material-symbols-outlined text-[20px]">delete</span></button>
                                    <button className="p-2 text-on-surface-variant hover:bg-surface-container-high transition-colors rounded-full"><span className="material-symbols-outlined text-[20px]">more_vert</span></button>
                                </div>
                            </td>
                        </tr>

                        <tr className="hover:bg-surface-container-low transition-colors group">
                            <td className="px-6 py-4">
                                <div className="flex items-center gap-3">
                                    <div className="w-10 h-10 rounded flex items-center justify-center bg-secondary-container/30 text-secondary">
                                        <span className="material-symbols-outlined">description</span>
                                    </div>
                                    <span className="font-body-md text-on-surface font-medium">Brand_Guidelines.docx</span>
                                </div>
                            </td>
                            <td className="px-6 py-4 text-on-surface-variant text-body-md">Oct 05, 2023</td>
                            <td className="px-6 py-4 text-on-surface-variant text-body-md">1.2 MB</td>
                            <td className="px-6 py-4 text-right">
                                <div className="flex justify-end gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                                    <button className="p-2 text-on-surface-variant hover:text-primary transition-colors"><span className="material-symbols-outlined text-[20px]">download</span></button>
                                    <button className="p-2 text-on-surface-variant hover:text-error transition-colors"><span className="material-symbols-outlined text-[20px]">delete</span></button>
                                    <button className="p-2 text-on-surface-variant hover:bg-surface-container-high transition-colors rounded-full"><span className="material-symbols-outlined text-[20px]">more_vert</span></button>
                                </div>
                            </td>
                        </tr>

                    </tbody>
                </table>
            </div>

            <div className="px-6 py-4 bg-surface-container-lowest border-t border-outline-variant flex justify-between items-center">
                <span className="text-label-sm text-on-surface-variant">Showing 4 of 128 files</span>
                <div className="flex gap-2">
                    <button className="p-2 border border-outline-variant rounded hover:bg-surface-container-low transition-colors disabled:opacity-50" disabled>
                        <span className="material-symbols-outlined text-[18px]">chevron_left</span>
                    </button>
                    <button className="p-2 border border-outline-variant rounded hover:bg-surface-container-low transition-colors">
                        <span className="material-symbols-outlined text-[18px]">chevron_right</span>
                    </button>
                </div>
            </div>
        </section>
    )
}

export default ListFiles