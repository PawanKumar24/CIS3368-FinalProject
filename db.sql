CREATE TABLE cargo (
  id INT AUTO_INCREMENT PRIMARY KEY,
  weight FLOAT NOT NULL,
  cargotype VARCHAR(255) NOT NULL,
  departure DATE,
  arrival DATE,
  shipid INT,
  FOREIGN KEY (shipid) REFERENCES spaceship(id),
  CHECK (weight > 0),
  CHECK (cargotype IN ('machinery', 'food', 'vehicles', 'raw materials'))
);

CREATE TABLE spaceship (
  id INT NOT NULL AUTO_INCREMENT,
  maxweight FLOAT NOT NULL,
  captainid INT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (captainid) REFERENCES captain(id)
);

CREATE TABLE captain (
    id INT AUTO_INCREMENT,
    firstname VARCHAR(50),
    lastname VARCHAR(50),
    rank VARCHAR(50),
    homeplanet VARCHAR(50),
    PRIMARY KEY (id)
);
