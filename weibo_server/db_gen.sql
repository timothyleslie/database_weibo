use weibo;
-- create table ARTICLE
-- (
--    A_ID                 int not null auto_increment,
--    U_ID                 int not null,
--    A_TIME               datetime not null default current_timestamp(0),
--    A_CONTENT            varchar(300) not null,
--    LIKE_CNT             int null default 0,
--    FAVORITE_CNT         int null default 0,
--    COMMENT_CNT          int null default 0,
--    TRANSMIT_ID          int null default 0,
--    primary key (A_ID)
-- );

-- create table USER
-- (
--    U_ID                 int not null auto_increment,
--    U_PASSWORD           varchar(20) not null,
--    U_NAME               varchar(15) not null,
--    primary key (U_ID)
-- );

-- create table LIKES
-- (
--    U_ID                 int not null,
--    A_ID                 int not null,
--    L_TIME               datetime not null default current_timestamp(0),
--    primary key (U_ID, A_ID)
-- );

-- create table FAVORITE
-- (
--    U_ID                 int not null,
--    A_ID                 int not null,
--    F_TIME               datetime not null default current_timestamp(0),
--    primary key (U_ID, A_ID)
-- );


-- create table TRANSMIT
-- (
--    U_ID                 int not null,
--    ORIGIN_A_ID          int not null,
--    NEW_A_ID             int not null,
--    T_TIME               datetime not null default current_timestamp(0),
--    primary key (U_ID, ORIGIN_A_ID, NEW_A_ID)
-- );


-- create table COMMENTS
-- (
--    C_ID                 int not null auto_increment,
--    C_TIME               datetime not null default current_timestamp(0),
--    U_ID                 int not null,
--    A_ID                 int not null,
--    C_CONTENT            varchar(300) not null,
--    primary key (C_ID)
-- );


-- create table CONCERN
-- (
--    CONCERN_U_ID         int not null,
--    CONCERNED_U_ID       int not null,
--    primary key (CONCERN_U_ID, CONCERNED_U_ID)
-- );

-- create table PRIVATE_MESSAGE
-- (
--    MSG_ID               int not null auto_increment,
--    SENDER_U_ID          int not null,
--    RECEIVER_U_ID       int not null,
--    MSG_TIME             datetime not null default current_timestamp(0),
--    MSG_CONTENT          varchar(300) not null,
--    primary key (MSG_ID)
-- );

-- alter table ARTICLE add constraint FK_POST foreign key (U_ID)
--       references USER (U_ID) on delete restrict on update restrict;

-- alter table COMMENTS add constraint FK_RELATIONSHIP_1 foreign key (U_ID)
--       references USER (U_ID) on delete restrict on update restrict;

-- alter table COMMENTS add constraint FK_RELATIONSHIP_2 foreign key (A_ID)
--       references ARTICLE (A_ID) on delete restrict on update restrict;

-- alter table CONCERN add constraint FK_CONCERN foreign key (CONCERNED_U_ID)
--       references USER (U_ID) on delete restrict on update restrict;

-- alter table CONCERN add constraint FK_CONCERN2 foreign key (CONCERN_U_ID)
--       references USER (U_ID) on delete restrict on update restrict;

-- alter table FAVORITE add constraint FK_FAVORITE foreign key (A_ID)
--       references ARTICLE (A_ID) on delete restrict on update restrict;

-- alter table FAVORITE add constraint FK_FAVORITE2 foreign key (U_ID)
--       references USER (U_ID) on delete restrict on update restrict;

-- alter table LIKES add constraint FK_LIKES foreign key (A_ID)
--       references ARTICLE (A_ID) on delete restrict on update restrict;

-- alter table LIKES add constraint FK_LIKES2 foreign key (U_ID)
--       references USER (U_ID) on delete restrict on update restrict;

-- alter table PRIVATE_MESSAGE add constraint FK_RECEIVE foreign key (RECEIVER__U_ID)
--       references USER (U_ID) on delete restrict on update restrict;

-- alter table PRIVATE_MESSAGE add constraint FK_SEND foreign key (SENDER_U_ID)
--       references USER (U_ID) on delete restrict on update restrict;

-- alter table TRANSMIT add constraint FK_TRANSMIT foreign key (ORIGIN_A_ID)
--       references ARTICLE (A_ID) on delete restrict on update restrict;

-- alter table TRANSMIT add constraint FK_TRANSMIT2 foreign key (U_ID)
--       references USER (U_ID) on delete restrict on update restrict;


-- CREATE VIEW view_article AS 
-- select A_ID,U_NAME,A_CONTENT,A_TIME, LIKE_CNT, FAVORITE_CNT, COMMENT_CNT 
-- from user, article 
-- where user.U_ID = article.U_ID order by A_TIME desc;
