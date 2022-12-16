const config = {
    screens: {
        Auth: {
            path: "auth"
        },
        Home: {
            path: "home"
        }
    }
}

const linking = {
    prefixes: ["demo://app"],
    config
}

export default linking;