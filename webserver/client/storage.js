class StorageItem {
    constructor(name, def = {}) {
        this.storage = window.localStorage;
        this.name = name;
        this.value = StorageItem.load(this.storage, name, def);
        this.def = def;
        this.save();
    };

    save() {
        this.storage.setItem(this.name, this.as_string());
    };

    get(name) {
        return this.value[name];
    };

    reset() {
        this.value = this.def;
        this.save();
    };

    set(name, value) {
        this.value[name] = value;
        this.save();
    }

    static load(storage, name, def = {}) {
        const previous_value = storage.getItem(name);
        if (previous_value) {
            return JSON.parse(previous_value);
        }
        return def;
    };

    as_string() {
        return JSON.stringify(this.value);
    };
};

export default StorageItem;