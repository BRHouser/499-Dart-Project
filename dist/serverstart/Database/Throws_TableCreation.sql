-- SQLite

CREATE TABLE Throws(id str,
MatchID str,
MatchName str,
Player1ID str,
Player2ID str,
legNumber str,
Turn str,
Throws str,
Score str,
foreign key (MatchID) references List_Matches(id),
foreign key (MatchName) references List_Matches(MatchName),
foreign key (Player1ID) references List_of_Players(id),
foreign key (Player2ID) references List_of_Players(id)
);

drop table Throws