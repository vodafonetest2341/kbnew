CREATE TABLE [knowledgebase].[Embeddings] (
    [ID]             INT             IDENTITY (1, 1) NOT NULL,
    [ContentId]      INT             NOT NULL,
    [ChunkedContent] VARCHAR (4000)  NOT NULL,
    [PageSource]     VARCHAR (4000)  NOT NULL,
    [Vectors]        VARBINARY (MAX) NOT NULL,
    [CreatedAt]      DATETIME        NULL,
    PRIMARY KEY CLUSTERED ([ID] ASC),
    CONSTRAINT [ContentID_FK1] FOREIGN KEY ([ContentId]) REFERENCES [knowledgebase].[Content] ([ID])
);


GO

