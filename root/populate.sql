

INSERT INTO Users(username, password, first_name, second_name)
VALUES
	('puy-puy', '123456', 'Катя', 'Прокопенко'),
	('user1', '654321', 'Петя', 'Маслов'),
	('slandkiivarenik', 'qwerty', 'Миша', 'Сидоров');

SELECT * FROM Users;



INSERT INTO Messenger(messenger_id, messenger_name)
VALUES
	(1, 'Telegram'),
	(2, 'Viber'),
	(3, 'Whatsapp');

SELECT * FROM Messenger;



INSERT INTO User_messengers(username, messenger)
VALUES
	('puy-puy', 1),
	('puy-puy', 2),
	('user1', 1);
	
	
INSERT INTO User_messengers(username, messenger)
VALUES
	('slandkiivarenik', 1);

SELECT * FROM User_messengers;




INSERT INTO Message(recipient, sender, messenger, content)
VALUES
	('puy-puy', 'user1', 1, 'Привет)' ),
	('user1', 'puy-puy', 1, 'Привет, как дела?'),
	('slandkiivarenik', 'user1', 1, 'Зайди домой');

SELECT * FROM Message;




INSERT INTO Clicks (message)
VALUES (1), (3);

INSERT INTO Clicks (message)
VALUES (1);

SELECT * FROM Clicks;

INSERT INTO Catagory (catagory_name, population)
VALUES
	('sport', 0),
	('travelling', 0),
	('job', 0);
	
SELECT * FROM Catagory;


