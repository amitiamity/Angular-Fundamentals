public static Configuration fromObject(Object obj) {
    Configuration config = new Configuration();

    for (Field field : obj.getClass().getDeclaredFields()) {
        field.setAccessible(true);

        try {
            Object value = field.get(obj);
            if (value == null) continue;

            // Get the key to use
            String key;
            ConfigKey annotation = field.getAnnotation(ConfigKey.class);
            if (annotation != null) {
                key = annotation.value();
            } else {
                key = field.getName().replace('_', '.'); // Fallback
            }

            // Handle types
            if (value instanceof Enum<?> e) {
                config.setString(key, e.name()); // Save enum name as string
            } else if (value instanceof String s) {
                config.setString(key, s);
            } else if (value instanceof Integer i) {
                config.setInteger(key, i);
            } else if (value instanceof Boolean b) {
                config.setBoolean(key, b);
            } else if (value instanceof Long l) {
                config.setLong(key, l);
            } else if (value instanceof Duration d) {
                config.set(key, ConfigOptions.key(key).durationType().defaultValue(d), d);
            } else {
                config.setString(key, value.toString()); // fallback
            }

        } catch (IllegalAccessException e) {
            throw new RuntimeException("Error reading config field: " + field.getName(), e);
        }
    }

    return config;
}
