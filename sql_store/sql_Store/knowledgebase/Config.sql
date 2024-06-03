CREATE TABLE [knowledgebase].[Config] (
    [ID]    INT           IDENTITY (1, 1) NOT NULL,
    [Name]  VARCHAR (250) NULL,
    [Value] VARCHAR (250) NULL,
    PRIMARY KEY CLUSTERED ([ID] ASC)
);


GO

