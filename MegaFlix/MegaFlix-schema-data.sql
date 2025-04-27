CREATE TABLE MegaFlix (
    id INT PRIMARY KEY,
    title VARCHAR(500),
    vote_average DECIMAL(3, 1),
    vote_count INT,
    status VARCHAR(50),
    release_date DATE,
    revenue BIGINT,
    runtime INT,
    adult BOOLEAN,
    backdrop_path VARCHAR(500),
    budget BIGINT,
    homepage VARCHAR(500),
    imdb_id VARCHAR(20),
    original_language VARCHAR(10),
    original_title VARCHAR(500),
    overview TEXT,
    popularity DECIMAL(6, 3),
    poster_path VARCHAR(500),
    tagline VARCHAR(500),
    genres VARCHAR(500),
    production_companies VARCHAR(500),
    production_countries VARCHAR(500),
    spoken_languages VARCHAR(500),
    keywords VARCHAR(500)
);

CREATE TABLE login(
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    mail TEXT NOT NULL,
    password TEXT NOT NULL
)  ;     
        
CREATE TABLE historique (
    listed_in TEXT,    
    id_user INT NOT NULL,               -- L'ID de l'utilisateur 
    date_heure TIMESTAMP DEFAULT CURRENT_TIMESTAMP,     -- Date et heure de l'événement
    type VARCHAR(100) NOT NULL,         -- Type d'action ou d'événement
    FOREIGN KEY (id_user) REFERENCES login(id)  -- Clé étrangère pointant vers la table `login`
);


CREATE TABLE favoris (
    id_favoris SERIAL PRIMARY KEY,
    id INT NOT NULL,                        -- Modifier ici pour correspondre au type INT de MegaFlix(id)
    title VARCHAR(255) NOT NULL,
    id_user INT NOT NULL,
    FOREIGN KEY (id_user) REFERENCES login(id),
    FOREIGN KEY (id) REFERENCES MegaFlix(id)
);

