function NavBar() {
    return (
        <nav className="sticky top-0 w-full z-50 flex justify-between items-center px-gutter h-16 bg-surface-container-lowest border-b border-outline-variant">
            <div className="flex items-center gap-8">
            <span className="text-headline-md font-headline-md text-primary">CloudVault</span>
            </div>
            <span className="text-body-md text-on-surface-variant font-medium">Welcome, Alex</span>
        </nav>
    )
}

export default NavBar