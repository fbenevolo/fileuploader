function StorageUsage() {
    return (
        <div className="grid grid-cols-12 gap-stack-lg mb-stack-lg">
            <div className="col-span-12 lg:col-span-8 flex flex-col justify-end">
              <h1 className="font-headline-lg text-headline-lg text-on-surface">Overview</h1>
              <p className="text-on-surface-variant mt-1">Manage your professional documents and media files securely.</p>
            </div>
            <div className="col-span-12 lg:col-span-4">
              <div className="bg-surface-container-lowest p-stack-md rounded-xl border border-outline-variant">
                <div className="flex justify-between items-center mb-4">
                  <span className="font-headline-md text-sm text-on-surface">Storage Status</span>
                  <span className="text-label-sm text-primary">75%</span>
                </div>
                <div className="w-full h-2 bg-surface-container rounded-full overflow-hidden mb-3">
                  <div className="h-full bg-primary" style={{ width: '75%' }}></div>
                </div>
                <div className="flex justify-between items-baseline">
                  <p className="text-body-md text-on-surface-variant"><span className="font-bold text-on-surface">15.2 GB</span> of 20 GB used</p>
                  <button className="text-primary font-button text-xs hover:underline">Upgrade</button>
                </div>
              </div>
            </div>
          </div>
    )
}

export default StorageUsage